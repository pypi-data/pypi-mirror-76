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
        while count <= end_year:
            year.append(str(count))
            count = count + interval
        self.year = year

    def set_region(self, regions):
        """ Sets the datacase's regions analysis

        Args:
            regions (list): list of regions 
        """
        self.regions = regions

    def set_emission(self, emissions):
        """Sets the cases emission types

        Args:
            emissions (List): list of emission types
        """
        self.emissions = emissions

    def set_technology(self, technology):
        """ Sets the cases technology type

        Args:
            technology (list): List of technologies
        """
        self.technology = technology

    def set_fuel(self, fuel):
        """ Sets the case's fuel types

        Args:
            fuel (list): list of fuels
        """
        self.fuel = fuel

    def set_timeslice(self, timeslice):
        """ Set of timeslices

        Args:
            timeslice (list): list of timeslices
        """
        self.timeslice = timeslice

    def set_mode_of_operation(self, num_modes_of_operation):
        """ Create the number of modes of operation (n = 1,...,num_modes_of_operation)

        Args:
            num_modes_of_operation (int): 
        """
        # Create set of mode_of_operation
        mode_of_operation = []
        count = 1
        while count <= num_modes_of_operation:
            mode_of_operation.append(str(count))
            count = count + 1
        self.mode_of_operation = mode_of_operation

    def set_storage(self, storage):
        """ Sets storage set of the datacase

        Args:
            storage (list): list of storage types
        """
        self.storage = storage

    def set_daytype(self, num_daytypes):
        """[summary]

        Args:
            num_daytypes (int): Number of daytypes
        """
        # Create set of daytypes
        daytype = []
        count = 1
        while count <= num_daytypes:
            daytype.append(str(count))
            count = count + 1
        self.daytype = daytype

    def set_season(self, num_seasons):
        """ Creates set of seasons

        Args:
            num_seasons (int): Number of seasons
        """
        # Create set of seasons
        season = []
        count = 1
        while count <= num_seasons:
            season.append(str(count))
            count = count + 1
        self.season = season

    def set_daily_time_bracket(self, num_dailytimebrackets):
        """ Creates set of daily time brackets

        Args:
            dailytimebracket (int): [description]
        """
        # Create set of dailytimebrackets
        dailytimebracket = []
        count = 1
        while count <= num_dailytimebrackets:
            dailytimebracket.append(str(count))
            count = count + 1
        self.dailytimebracket = dailytimebracket

    # Functions to define the parameters moving forward.
    def set_year_split(self, YearSplit):
        """ Sets the 2D parameter YearSplit

        Args:
            yearsplit (int): 2D Matrix of Timeslice Partitions
        """
        self.YearSplit = YearSplit

    def set_discount_rate(self, parameters):
        """ Calculates the effective tax rates for each region

        Args:
            parameters ([type]): [description]
        """

        self.DaySplit = None

    def set_day_split(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_conversation_ls(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_conversion_ld(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_conversion_lh(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_days_in_day_type(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_trade_route(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_depreciation_method(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_specified_annual_demand(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_specified_demand_profile(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_accumulated_annual_demand(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_capacity_to_activity_unit(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_capacity_factor(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_availability_factor(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_operational_life(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_residual_capacity(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_input_activity_ratio(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_output_activity_ratio(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_capital_cost(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_variable_cost(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_fixed_cost(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_technology_to_storage(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_technology_from_storage(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_min_storage_charge(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_operational_life_storage(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_capital_cost_storage(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_storage_level_start(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_storage_max_charge_rate(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_storage_max_discharge_rate(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_residual_storage_capacity(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """
        self.ResidualStorageCapacity = None

    def set_capacity_of_one_technology_unit(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_total_annual_max_capacity(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_total_annual_min_capacity(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_total_technology_annual_activity_lower_limit(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_total_technology_annual_activity_upper_limit(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_total_technology_period_activity_upper_limit(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_total_technology_period_activity_lower_limit(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_reserve_margin_tag_technology(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_reserve_margin_tag_fuel(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_reserve_margin(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_re_tag_technology(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_re_tag_fuel(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_re_min_production_target(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_emission_activity_ratio(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_emissions_penalty(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_annual_exogenous_emission(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_annual_emission_limit(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_model_period_exogenous_emission(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """

    def set_model_period_emission_limit(self, parameters):
        """[summary]

        Args:
            parameters ([type]): [description]
        """