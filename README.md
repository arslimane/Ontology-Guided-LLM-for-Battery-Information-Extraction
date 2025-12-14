# Ontology-Guided Large Language Model Pipeline for Structured Information Extraction from Battery Cell Datasheets

This repository contains the **official code implementation** accompanying the paper accepted at **NeuroSym4MLLM – EGC 2026 Atelier**  
(*Neuro-symbolique et connaissances pour les LLMs multimodaux*).

---

## 📄 Paper Overview

Automatic information extraction from battery cell datasheets is critical for accurate modeling and performance management of electrochemical cells.  However, these datasheets are typically distributed as **unstructured PDF documents**, making automated exploitation challenging.
This work introduces a **complete ontology-guided extraction pipeline** that leverages **Large Language Models (LLMs)** to transform heterogeneous datasheet content into **structured, queryable knowledge**.

### Key Ideas
- Use of a **battery domain ontology** to guide extraction
- A **dual-LLM pipeline** combining:
  - Chain-of-Thought reasoning
  - Few-shot learning
- Extraction of **structured RDF-like triples**
- An **LLM-based validation step** to:
  - Enforce ontology compliance
  - Remove duplicates
  - Correct invalid or inconsistent triples

We evaluate **five different LLMs** across multiple battery cell datasheets. Extracted triples are manually verified, demonstrating that recent LLMs significantly improve both **accuracy** and **structural consistency** when combined with an ontology-driven approach.

---

## 📚 Citation

If you use this code or build upon this work, please cite the following paper:

```bibtex
@inproceedings{arbaoui2026ontology,
  title     = {Ontology-Guided Large Language Model Pipeline for Structured Information Extraction from Battery Cell Datasheets},
  author    = {Slimane Arbaoui, Ali Ayadi, Ahmed Samet, Tedjani Mesbahi and Romuald Boné},
  booktitle = {NeuroSym4MLLM Workshop, EGC 2026},
  year      = {2026}
}
