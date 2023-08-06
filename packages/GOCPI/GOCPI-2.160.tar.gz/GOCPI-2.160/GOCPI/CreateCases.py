import os
import numpy as np
import pandas as pd


class CreateCases:
    """ A class of methods to create user-defined data cases
    """
    def __unit__(self):
        """ Sets the parameters and sets for the datacase
        """
        # Sets (placeholders for setting values)
        self.year = None
        self.region = None
        self.emission = None
        self.technology = None
        self.fuel = None
        self.timeslice = None
        self.mode_of_operation = None
        self.storage = None
        self.daytype = None
        self.season = None
        self.dailytimebracket = None

        # Parameters
        self.YearSplit = None
        self.DiscountRate = None
        self.DaySplit = None
        self.Conversionls = None
        self.Conversionld = None
        self.Conversionlh = None
        self.DaysInDayType = None
        self.TradeRoute = None
        self.DepreciationMethod = None
        self.SpecifiedAnnualDemand = None
        self.SpecifiedDemandProfile = None
        self.AccumulatedAnnualDemand = None
        self.CapacityToActivityUnit = None
        self.CapacityFactor = None
        self.AvailabilityFactor = None
        self.OperationalLife = None
        self.ResidualCapacity = None
        self.InputActivityRatio = None
        self.OutputActivityRatio = None
        self.CapitalCost = None
        self.VariableCost = None
        self.FixedCost = None
        self.TechnologyToStorage = None
        self.TechnologyFromStorage = None
        self.StorageLevelStart = None
        self.StorageMaxChargeRate = None
        self.StorageMaxDischargeRate = None
        self.MinStorageCharge = None
        self.OperationalLifeStorage = None
        self.CapitalCostStorage = None
        self.ResidualStorageCapacity = None
        self.CapacityOfOneTechnologyUnit = None
        self.TotalAnnualMaxCapacity = None
        self.TotalAnnualMinCapacity = None
        self.TotalAnnualMaxCapacityInvestment = None
        self.TotalAnnualMinCapacityInvestment = None
        self.TotalTechnologyAnnualActivityLowerLimit = None
        self.TotalTechnologyAnnualActivityUpperLimit = None
        self.TotalTechnologyModelPeriodActivityUpperLimit = None
        self.TotalTechnologyModelPeriodActivityLowerLimit = None
        self.ReserveMarginTagTechnology = None
        self.ReserveMarginTagFuel = None
        self.ReserveMargin = None
        self.RETagTechnology = None
        self.RETagFuel = None
        self.REMinProductionTarget = None
        self.EmissionActivityRatio = None
        self.EmissionsPenalty = None
        self.AnnualExogenousEmission = None
        self.AnnualEmissionLimit = None
        self.ModelPeriodExogenousEmission = None
        self.ModelPeriodEmissionLimit = None

    def set_year(self, start_year, end_year, interval):
        """ Sets a list of forecast years

        Args:
            start_year (int): Starting year for forecasting (Less than end_year)
            end_year (int): Ending year for forecasting (Greater than start_year)
            interval (int): Gap for forecasting period
        """
        # Sets year array for new value
        year = []
        count = start_year
        while count < end_year:
            year.append(str(count))
            count = count + interval
        self.year = year

    def set_region(self, regions):
        """ Sets the datacases regions of analysis

        Args:
            regions (list): list
        """

    def set_emission(self, emissions):
        """[summary]

        Args:
            emissions (List): [description]
        """