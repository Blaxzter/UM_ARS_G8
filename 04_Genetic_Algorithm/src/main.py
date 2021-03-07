import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from genetic.GeneticAlgorithm import GeneticAlgorithm

if __name__ == '__main__':
    # gen_alg = GeneticAlgorithm(
    #     load='data/chromosome_20210307-163657_data.json',
    #     generation=219,
    #     # show_best=-1,
    #     room = [0, 2, 5]
    # )
    gen_alg = GeneticAlgorithm()
    gen_alg.run()
