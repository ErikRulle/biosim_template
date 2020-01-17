# -*- coding: utf-8 -*-

"""
"""

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


import biosim.island as bi
import random
import pandas as pd


class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing
        animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal
        densities
        :param img_base: String with beginning of file name for figures,
        including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        random.seed(seed)
        self.last_year_simulated = 0
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.island = bi.Island(island_map=island_map)
        self.island.populate_the_island(ini_pop)
        self.herbivore_list = [self.island.total_island_population[0]]
        self.carnivore_list = [self.island.total_island_population[1]]
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        species.set_animal_parameters(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        landscape.set_landscape_parameters(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
        (default: vis_years)

        Image files will be numbered consecutively.
        """
        for _ in range(num_years):
            new_island_population = self.island.annual_cycle()
            self.herbivore_list.append(new_island_population[0])
            self.carnivore_list.append(new_island_population[1])

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.populate_the_island(population)

    @property
    def year(self):
        """
        Last year simulated.
        """
        return self.last_year_simulated

    @property
    def num_animals(self):
        """
        Total number of animals on island.
        """
        return self.herbivore_list[-1] + self.carnivore_list[-1]

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.
        """
        animal_dict = {"Herbivores": self.island.total_island_population[0],
                       "Carnivore": self.island.total_island_population[1]}
        return animal_dict

    @property
    def animal_distribution(self):
        """
        Pandas DataFrame with animal count per species for each cell on island.
        """
        pandas_population = pd.DataFrame(self.island.population_in_each_cell,
                                         columns=["Herbivores", "Carnivores"])
        return pandas_population

    def make_movie(self):
        """
        Create MPEG4 movie from visualization images saved.
        """
