import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from src.genetic.GeneticAlgorithm import GeneticAlgorithm

if __name__ == '__main__':
    # gen_alg = GeneticAlgorithm(
    #     load = 'data/chromosome_20210306-190854_data.json',
    #     generation = -1,
    #     show_best = 1,
    #     # room = 1
    # )
    gen_alg = GeneticAlgorithm()
    gen_alg.run()


