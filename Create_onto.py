from owlready2 import *

# -----------------------------------------
# Create ontology
# -----------------------------------------
onto = get_ontology("http://example.org/battery_cell_ontology.owl")

with onto:

    # -----------------------------------------
    # Top-Level Classes
    # -----------------------------------------
    class BatteryCell(Thing): pass
    class Manufacturer(Thing): pass
    class Specification(Thing): pass
    class ElectricalProperty(Thing): pass
    class ThermalProperty(Thing): pass
    class MechanicalProperty(Thing): pass
    class SafetyProperty(Thing): pass
    class PerformanceProperty(Thing): pass
    class CycleLife(Thing): pass
    class C_RatePerformance(Thing): pass
    class Electrochemistry(Thing): pass
    class CellType(Thing): pass
    class Dimension(Thing): pass
    class Mass(Thing): pass
    class OperatingCondition(Thing): pass
    class EnvironmentalCondition(Thing): pass
    class Material(Thing): pass
    class Certification(Thing): pass

    # -----------------------------------------
    # Object Properties
    # -----------------------------------------
    class hasManufacturer(BatteryCell >> Manufacturer): pass
    class hasSpecification(BatteryCell >> Specification): pass
    
    class hasElectricalProperty(BatteryCell >> ElectricalProperty): pass
    class hasThermalProperty(BatteryCell >> ThermalProperty): pass
    class hasMechanicalProperty(BatteryCell >> MechanicalProperty): pass
    class hasSafetyProperty(BatteryCell >> SafetyProperty): pass
    class hasPerformanceProperty(BatteryCell >> PerformanceProperty): pass
    
    class hasElectrochemistry(BatteryCell >> Electrochemistry): pass
    class hasCellType(BatteryCell >> CellType): pass
    class hasMaterial(BatteryCell >> Material): pass
    class hasCathodeMaterial(BatteryCell >> Material): pass
    class hasAnodeMaterial(BatteryCell >> Material): pass

    class hasChargeSpecification(BatteryCell >> Specification): pass
    class hasDischargeSpecification(BatteryCell >> Specification): pass

    class hasCycleLife(BatteryCell >> CycleLife): pass
    class hasCRatePerformance(BatteryCell >> C_RatePerformance): pass
    
    class hasDimension(BatteryCell >> Dimension): pass
    class hasMass(BatteryCell >> Mass): pass
    
    class hasOperatingCondition(BatteryCell >> OperatingCondition): pass
    class hasEnvironmentalCondition(BatteryCell >> EnvironmentalCondition): pass
    
    class hasCertification(BatteryCell >> Certification): pass

    # -----------------------------------------
    # Data Properties
    # -----------------------------------------
    class hasModelName(BatteryCell >> str): pass
    class hasNominalVoltage(BatteryCell >> float): pass
    class hasNominalCapacity(BatteryCell >> float): pass
    class hasMinimumCapacity(BatteryCell >> float): pass
    class hasInternalResistance(BatteryCell >> float): pass

    # Energy density
    class hasEnergyDensityGravimetric(BatteryCell >> float): pass
    class hasEnergyDensityVolumetric(BatteryCell >> float): pass

    # Voltage limits
    class hasChargeCutoffVoltage(BatteryCell >> float): pass
    class hasDischargeCutoffVoltage(BatteryCell >> float): pass
    class hasOperatingVoltageRangeMin(BatteryCell >> float): pass
    class hasOperatingVoltageRangeMax(BatteryCell >> float): pass

    # Current limits
    class hasStandardChargeCurrent(BatteryCell >> float): pass
    class hasFastChargeCurrent(BatteryCell >> float): pass
    class hasMaxContinuousDischargeCurrent(BatteryCell >> float): pass
    class hasPulseDischargeCurrent(BatteryCell >> float): pass

    # Thermal properties
    class hasOperatingTemperatureChargeMin(BatteryCell >> float): pass
    class hasOperatingTemperatureChargeMax(BatteryCell >> float): pass
    class hasOperatingTemperatureDischargeMin(BatteryCell >> float): pass
    class hasOperatingTemperatureDischargeMax(BatteryCell >> float): pass
    class hasStorageTemperatureMin(BatteryCell >> float): pass
    class hasStorageTemperatureMax(BatteryCell >> float): pass

    # Mechanical properties
    class hasDiameter(Dimension >> float): pass
    class hasWidth(Dimension >> float): pass
    class hasHeight(Dimension >> float): pass
    class hasThickness(Dimension >> float): pass
    class hasLength(Dimension >> float): pass
    class hasVolume(Dimension >> float): pass

    class hasWeight(Mass >> float): pass

    # Safety properties
    class hasOverchargeTolerance(BatteryCell >> float): pass
    class hasShortCircuitBehavior(BatteryCell >> str): pass
    class hasPenetrationTestResult(BatteryCell >> str): pass
    class hasCrushTestResult(BatteryCell >> str): pass
    class hasVentMechanismPresence(BatteryCell >> bool): pass
    class hasUN38_3Certification(BatteryCell >> bool): pass
    class hasIEC62133Certification(BatteryCell >> bool): pass
    class hasULCertification(BatteryCell >> bool): pass

    # Performance properties
    class hasNumberOfCycles(CycleLife >> int): pass
    class hasEndOfLifeCapacityPercent(CycleLife >> float): pass
    class hasCycleTestTemperature(CycleLife >> float): pass

    class hasChargeCRate(C_RatePerformance >> float): pass
    class hasDischargeCRate(C_RatePerformance >> float): pass
    class hasCapacityRetentionAtCRate(C_RatePerformance >> float): pass


    # Metadata
    class hasSourcePDF(BatteryCell >> str): pass

# -----------------------------------------
# Save the ontology
# -----------------------------------------
onto.save("battery_cell_ontology.owl")
print("Ontology saved as battery_cell_ontology.owl")
