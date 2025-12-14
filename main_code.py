import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np
import pandas as pd
from rdflib import Graph
from PyPDF2 import PdfReader
import logging
import gc
import json
from owlready2 import get_ontology, Thing
import outlines
from outlines.types import JsonSchema
# Complete list of ontology classes
ontology_classes = [
    # Battery cell and related classes
    "BatteryCell",
    "Manufacturer",
    "Specification",
    "ElectricalProperty",
    "ThermalProperty",
    "MechanicalProperty",
    "SafetyProperty",
    "PerformanceProperty",
    "CycleLife",
    "C_RatePerformance",
    "Electrochemistry",
    "CellType",
    "Dimension",
    "Mass",
    "OperatingCondition",
    "EnvironmentalCondition",
    "Material",
    "Certification"
]
ontology_properties = [
    # Object properties
    "hasManufacturer",
    "hasSpecification",
    "hasElectricalProperty",
    "hasThermalProperty",
    "hasMechanicalProperty",
    "hasSafetyProperty",
    "hasPerformanceProperty",
    "hasElectrochemistry",
    "hasCellType",
    "hasMaterial",
    "hasCathodeMaterial",
    "hasAnodeMaterial",
    "hasChargeSpecification",
    "hasDischargeSpecification",
    "hasCycleLife",
    "hasCRatePerformance",
    "hasDimension",
    "hasMass",
    "hasOperatingCondition",
    "hasEnvironmentalCondition",
    "hasCertification",

    # Data properties
    "hasModelName",
    "hasNominalVoltage",
    "hasNominalCapacity",
    "hasMinimumCapacity",
    "hasInternalResistance",
    "hasEnergyDensityGravimetric",
    "hasEnergyDensityVolumetric",
    "hasChargeCutoffVoltage",
    "hasDischargeCutoffVoltage",
    "hasOperatingVoltageRangeMin",
    "hasOperatingVoltageRangeMax",
    "hasStandardChargeCurrent",
    "hasFastChargeCurrent",
    "hasMaxContinuousDischargeCurrent",
    "hasPulseDischargeCurrent",
    "hasOperatingTemperatureChargeMin",
    "hasOperatingTemperatureChargeMax",
    "hasOperatingTemperatureDischargeMin",
    "hasOperatingTemperatureDischargeMax",
    "hasStorageTemperatureMin",
    "hasStorageTemperatureMax",
    "hasDiameter",
    "hasWidth",
    "hasHeight",
    "hasThickness",
    "hasLength",
    "hasVolume",
    "hasWeight",
    "hasOverchargeTolerance",
    "hasShortCircuitBehavior",
    "hasPenetrationTestResult",
    "hasCrushTestResult",
    "hasVentMechanismPresence",
    "hasUN38_3Certification",
    "hasIEC62133Certification",
    "hasULCertification",
    "hasNumberOfCycles",
    "hasEndOfLifeCapacityPercent",
    "hasCycleTestTemperature",
    "hasChargeCRate",
    "hasDischargeCRate",
    "hasCapacityRetentionAtCRate",
    "hasSourcePDF"
]

# Single triple schema
single_triple_schema = {
    "type": "object",
    "properties": {
        "Used_text": {"type": "string"},
        "head": {"type": "string"},
        "head_type": {"type": "string", "enum": ontology_classes},
        "relation": {"type": "string", "enum": ontology_properties},
        "tail": {"type": "string"},
        "tail_type": {"type": "string", "enum": ontology_classes + ["str", "float", "bool"]}
    },
    "required": ["Used_text", "head", "head_type", "relation", "tail", "tail_type"]
}

# Multiple triples schema: array of objects
kg_triples_schema = {
    "type": "array",
    "items": single_triple_schema
}

KGTripleSchema = JsonSchema(kg_triples_schema)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def load_model_llm(model_name):
    model = outlines.from_transformers(
        AutoModelForCausalLM.from_pretrained(model_name, device_map="auto"),
        AutoTokenizer.from_pretrained(model_name)
    )
    logging.info("Model loaded successfully.")
    return model

def Ask_LLM(prompt,model,KGTripleSchema,max_new_tokens):
    triples = model(prompt, KGTripleSchema, max_new_tokens=max_new_tokens,temperature=0.2,repetition_penalty=1.1)
    del model
    torch.cuda.empty_cache()
    gc.collect()
    return triples
def summarize_ontology_for_prompt(owl_file_path:str)->str:
    """
    Load an OWL ontology and generate a clean text summary .

    Returns:
        str: A nicely formatted text summary of classes, hierarchy, and properties.
    """
    onto = get_ontology(owl_file_path).load()

    # ---------------- Extract class hierarchy ----------------
    def get_hierarchy(cls):
        children = list(cls.subclasses())
        if children:
            hierarchy = {}
            for subcls in children:
                hierarchy.update(get_hierarchy(subcls))  
            return {cls.name: hierarchy}  
        else:
            return {cls.name: {}}  

    # Start from top-level classes (direct subclasses of Thing)
    hierarchy_summary = {}
    for cls in onto.classes():
        if Thing in cls.is_a and cls != Thing:
            hierarchy_summary.update(get_hierarchy(cls))

    # ---------------- Extract object and data properties ----------------
    obj_props = []
    data_props = []

    for prop in onto.object_properties():
        domains = [d.name for d in prop.domain]
        ranges = [r.name for r in prop.range]
        obj_props.append(f"- {prop.name}: domain={domains}, range={ranges}")

    for prop in onto.data_properties():
        domains = [d.name for d in prop.domain]
        ranges = [r.name if hasattr(r, 'name') else str(r) for r in prop.range]
        data_props.append(f"- {prop.name}: domain={domains}, range={ranges}")

    # ---------------- Convert hierarchy to readable text ----------------
    def hierarchy_to_text(h, level=0):
        text = ""
        for k, v in h.items():
            text += "  " * level + f"- {k}\n"
            text += hierarchy_to_text(v, level + 1)
        return text

    hierarchy_text = hierarchy_to_text(hierarchy_summary)

    # ---------------- Combine everything ----------------
    prompt_text = "Ontology Summary:\n\n"
    prompt_text += "Classes and Hierarchy:\n"
    prompt_text += hierarchy_text + "\n"
    prompt_text += "Object Properties:\n"
    prompt_text += "\n".join(obj_props) + "\n\n"
    prompt_text += "Data Properties:\n"
    prompt_text += "\n".join(data_props) + "\n"

    return prompt_text

def build_validation_prompt(candidates: str, chunk_text: str, ontology_summary: str) -> str:
    """
    Validate candidate triples for battery datasheet information only.
    """
    prompt = f"""
You are an expert validator for battery datasheet information. Your task is to strictly validate candidate triples.

RULES:

1. Keep only triples that describe **technical datasheet information**:
   - Electrical properties: voltage, capacity, charge/discharge limits, internal resistance
   - Mechanical properties: dimensions, mass
   - Materials & components: electrodes, electrolytes, separators
   - Cell type / chemistry
2. Verify that each entity exists in the text chunk.
3. Verify ontology alignment: head_type, tail_type, relation must exist in ontology.
4. Ignore all non-battery content (authors, references, journals, etc.)

Output ONLY a JSON array of objects with keys:
"Used_text", "head", "head_type", "relation", "tail", "tail_type"

Candidate triples:
{candidates}

Text chunk:
\"\"\"{chunk_text}\"\"\"

Ontology dictionary:
{ontology_summary}

Return ONLY the JSON array of validated datasheet triples.
"""
    return prompt
def Extract_Triplets_Cot_with2Shots_prompt(chunk_text: str, ontology_summary: str) -> str:
    """
    Returns a datasheet-focused prompt for ontology-guided triplet extraction
    using CoT and few-shot examples.
    """

    examples = [
        {
            "chunktext": (
                "The 18650 lithium-ion cell has a nominal voltage of 3.6V and a nominal capacity of 3000mAh."
            ),
            "Used_text": "The 18650 lithium-ion cell has a nominal voltage of 3.6V and a nominal capacity of 3000mAh",
            "head": "18650 LithiumIonCell",
            "head_type": "BatteryCell",
            "relation": "hasNominalVoltage",
            "tail": "3.6",
            "tail_type": "float",
        },
         {
            "chunktext": (
                "The 18650 lithium-ion cell has a nominal voltage of 3.6V and a nominal capacity of 3000mAh."
            ),
            "Used_text": "The 18650 lithium-ion cell has a nominal voltage of 3.6V and a nominal capacity of 3000mAh",
            "head": "18650 LithiumIonCell",
            "head_type": "BatteryCell",
            "relation": "hasNominalCapacity",
            "tail": "3000",
            "tail_type": "float",
        },
        {
            "chunktext": "The cell mass is 45 grams and the maximum charge voltage is 4.2V.",
            "Used_text": "The cell mass is 45 grams and the maximum charge voltage is 4.2V",
            "head": "LithiumIonCell",
            "head_type": "BatteryCell",
            "relation": "hasMass",
            "tail": "45",
            "tail_type": "float",
        }
    ]

    examples_str = "\n".join([
        f"Example:\n"
        f"chunktext: {ex['chunktext']}\n"
        f"Used_text: {ex['Used_text']}\n"
        f"head: {ex['head']}\n"
        f"head_type: {ex['head_type']}\n"
        f"relation: {ex['relation']}\n"
        f"tail: {ex['tail']}\n"
        f"tail_type: {ex['tail_type']}\n"
        for ex in examples
    ])

    prompt = f"""
You are a battery datasheet information extraction model. Your task is to extract **only technical datasheet information** such as:

- Electrical specifications: nominal voltage, capacity, charge/discharge limits, internal resistance
- Mechanical specifications: dimensions, mass
- Materials & components: electrodes, separators, electrolytes
- Cell type / chemistry

RULES:

1. Process the text sentence by sentence.
2. Map each entity to a class from the ontology dictionary.
3. Use only valid relations (object/data properties) from the ontology.
4. Normalize entity names to full canonical identifiers.
5. Return ONLY triples aligned with the ontology and found in the text.

Output format:
JSON array of objects with keys:
"Used_text", "head", "head_type", "relation", "tail", "tail_type"

Ontology dictionary (classes and relations):
{ontology_summary}

Few-shot examples:
{examples_str}

Text to analyze:
\"\"\"{chunk_text}\"\"\"

Return ONLY the JSON array of valid datasheet triples.
"""
    return prompt


def chunk_pdf_text(pdf_path: str, chunk_size: int = 1000,overlap: int = 200):
    """
    Reads a PDF file and splits its text into chunks of a specified size.

    Parameters:
        pdf_path (str): Path to the PDF file.
        chunk_size (int): Maximum number of characters per chunk.

    Returns:
        list[str]: A list containing text chunks.
    """
    # Read PDF
    reader = PdfReader(pdf_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    logging.info(f"PDF read complete, total length: {len(full_text)} chars.")
    # Split text into chunks
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        chunks.append(full_text[start:end])
        start += chunk_size - overlap
    logging.info(f"Split PDF into {len(chunks)} chunks (chunk_size={chunk_size}).")
    return chunks








def Total_pipline(pdf_file:str,oFile:str,ontology_file:str,model_name:str,chunk_size:int=1500,max_new_tokens:int=300):    
    logging.info("=== STARTING ONTOLOGY EXTRACTION PIPELINE ===")
    
    output_file = f"./Results/new_triplets_{oFile}.txt"
    # Load model
    model = load_model_llm(model_name)

    # Load ontology
    ontology_summary = summarize_ontology_for_prompt(ontology_file)

    # Chunk PDF
    chunks = chunk_pdf_text(pdf_file, chunk_size=chunk_size)

    # Process chunks
    Triplets=[]
    for i, chunk in enumerate(chunks, 1):
        logging.info(f"Processing chunk {i}/{len(chunks)}...")

        prompt = Extract_Triplets_Cot_with2Shots_prompt(chunk_text=chunk, ontology_summary=ontology_summary)
        output = Ask_LLM(prompt=prompt, model=model,KGTripleSchema=KGTripleSchema ,max_new_tokens=max_new_tokens)
        validation_prompt=build_validation_prompt(candidates=output,chunk_text=chunk,ontology_summary=ontology_summary)
        validated_output = Ask_LLM(prompt=validation_prompt, model=model,KGTripleSchema=KGTripleSchema ,max_new_tokens=max_new_tokens) #validate triples
        # Append results    
        try:
            Blocks = json.loads(validated_output)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON from LLM output: {e}")
            Blocks = []
        logging.info(f"Chunk {i} extracted :{len(Blocks)}")
        if(len(Blocks)!=0):
            Triplets.extend(Blocks)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"new_triples_:{Triplets}")  
    logging.info("Done :)")
        
    return Triplets

def getResultsCoT(model_name,pdf_file,ontofile,chunk_size,outputFile,max_new_tokens):
    Pdf_file=f"./Data/PdfFiles/{pdf_file}"
    ontology_file=f"./Data/Ontologies/{ontofile}"
    Triplets=Total_pipline(pdf_file=Pdf_file,oFile=outputFile,ontology_file=ontology_file,model_name=model_name,chunk_size=chunk_size,max_new_tokens=max_new_tokens)




if __name__ == "__main__":
    chunks=chunk_pdf_text("./Data/PdfFiles/p1.pdf")
    print(len(chunks[0]))
    chunk=chunks[0]
    ontology_summary = summarize_ontology_for_prompt("./Data/Ontologies/battery_cell_ontology.owl")
    print(ontology_summary)
        
