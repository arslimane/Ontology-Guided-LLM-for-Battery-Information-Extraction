from  owlready2  import *

# Load external Time ontology (if needed later)
#Time = get_ontology("https://www.w3.org/2006/time#")
#Time.load()


# Create your ontology
onto = get_ontology("./BatteryPhenomenon.owl")

with onto:
    # ---------------- BatteryPhenomenon hierarchy ----------------
    class BatteryPhenomenon(Thing):
        pass

    class bp_hasTextDescription(DataProperty):
        domain = [BatteryPhenomenon]
        range = [str]

    class isAnomaly(DataProperty):
        domain = [BatteryPhenomenon]
        range = [bool]
    class Consequence(Thing): pass
    class Recommendation(Thing): pass
    class Explanation(Thing): pass
    class CausalRelation(Thing): pass
    class Feature(Thing): pass
    class hasConsequence(ObjectProperty):
        domain = [BatteryPhenomenon]
        range = [Consequence]

    class leadsTo(ObjectProperty):
        domain = [BatteryPhenomenon]
        range = [BatteryPhenomenon]

    class hasMitigationRecommendation(ObjectProperty):
        domain = [BatteryPhenomenon]
        range = [Recommendation]

    class isExplainedBy(ObjectProperty):
        domain = [BatteryPhenomenon]
        range = [Explanation]

    # Phenomenon subtypes
    class MechanicalPhenomenon(BatteryPhenomenon): pass
    class ThermalPhenomenon(BatteryPhenomenon): pass
    class ElectricalPhenomenon(BatteryPhenomenon): pass
    class ElectrochemicalPhenomenon(BatteryPhenomenon): pass

    # MechanicalPhenomenon examples
    class SEI_growth(MechanicalPhenomenon): pass
    class SEI_decomposition(MechanicalPhenomenon): pass
    class Binder_decomposition(MechanicalPhenomenon): pass
    class Graphite_exfoliation(MechanicalPhenomenon): pass
    class Structure_disordering(MechanicalPhenomenon): pass
    class Lithium_plating_dendrite_formation(MechanicalPhenomenon): pass
    class Loss_of_electric_contact(MechanicalPhenomenon): pass
    class Electrode_particle_cracking(MechanicalPhenomenon): pass
    class Transition_metal_dissolution(MechanicalPhenomenon): pass
    class Current_collector_corrosion(MechanicalPhenomenon): pass

    # ThermalPhenomenon examples
    class Thermal_runaway(ThermalPhenomenon): pass
    class Overheating(ThermalPhenomenon): pass

    # ElectricalPhenomenon examples
    class Overcharging(ElectricalPhenomenon): pass
    class ShortCircuit(ElectricalPhenomenon): pass
    class Overdischarging(ElectricalPhenomenon): pass

    # ElectrochemicalPhenomenon examples
    class ElectrolyteDecomposition(ElectrochemicalPhenomenon): pass
    class LithiumPlating(ElectrochemicalPhenomenon): pass

    # ---------------- Explanation ----------------
    
    class exp_hasTextDescription(DataProperty):
        domain = [Explanation]
        range = [str]

    class representsCausalRelation(ObjectProperty):
        domain = [Explanation]
        range = [CausalRelation]

    # ---------------- CausalRelation ----------------
    
    class hasAffectedFeature(ObjectProperty):
        domain = [CausalRelation]
        range = [Feature]
    class hasCauseFeature(ObjectProperty):
        domain = [CausalRelation]
        range = [Feature]

    # ---------------- Recommendation ----------------
    
    class rec_hasTextDescription(DataProperty):
        domain = [Recommendation]
        range = [str]

    # ---------------- Consequence ----------------
    
    class CapacityDegradation(Consequence): pass
    class InternalResistanceIncrease(Consequence): pass
    class ThermalFailure(Consequence): pass
    class PerformanceDrop(Consequence): pass

    # ---------------- Feature ----------------
    
    class hasName(DataProperty):
        domain = [Feature]
        range = [str]

    # ---------------- Battery structure ----------------
    class BatteryPack(Thing): pass
    class BatteryModule(Thing): pass
    class BatteryCell(Thing): pass

    class LithiumIonCell(BatteryCell): pass
    class LeadAcidCell(BatteryCell): pass
    class NickelMetalHydrideCell(BatteryCell): pass
    class SolidStateCell(BatteryCell): pass

    class Lithium_Iron_Phosphate_Cell(LithiumIonCell): pass
    class Nickel_Manganese_Cobalt_Cell(LithiumIonCell): pass
    class Nickel_Cobalt_Aluminum_Cell(LithiumIonCell): pass

    # Components
    class Electrode(Thing): pass
    class Electrolyte(Thing): pass
    class Separator(Thing): pass

    # ObjectProperties for composition (no overwriting)
    class batteryPack_composedOfModule(ObjectProperty):
        domain = [BatteryPack]
        range = [BatteryModule]

    class module_composedOfCell(ObjectProperty):
        domain = [BatteryModule]
        range = [BatteryCell]

    class cell_hasElectrode(ObjectProperty):
        domain = [BatteryCell]
        range = [Electrode]

    class cell_hasElectrolyte(ObjectProperty):
        domain = [BatteryCell]
        range = [Electrolyte]

    class cell_hasSeparator(ObjectProperty):
        domain = [BatteryCell]
        range = [Separator]

    # Battery cell properties
    class hasNominalVoltage(DataProperty):
        domain = [BatteryCell]
        range = [float]

    class hasChargingCutOffVoltage(DataProperty):
        domain = [BatteryCell]
        range = [float]

    class hasDischargingCutOffVoltage(DataProperty):
        domain = [BatteryCell]
        range = [float]

    class hasNominalCapacity(DataProperty):
        domain = [BatteryCell]
        range = [float]

    # Corrected exhibits as ObjectProperty
    class exhibits(ObjectProperty):
        domain = [BatteryCell]
        range = [BatteryPhenomenon]

# Save ontology
onto.save(file="BatteryPhenomenon.owl", format="rdfxml")
