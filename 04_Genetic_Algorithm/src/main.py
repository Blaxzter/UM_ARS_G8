import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from genetic.GeneticAlgorithm import GeneticAlgorithm

if __name__ == '__main__':
    # gen_alg = GeneticAlgorithm(
    #     load = 'data/chromosome_20210307-153344_data.json',
    #     generation = -1,
    #     show_best = 3,
    #     room = 2
    # )
    gen_alg = GeneticAlgorithm()
    gen_alg.run()
