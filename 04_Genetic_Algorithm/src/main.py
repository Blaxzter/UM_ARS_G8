import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from src.genetic.GeneticAlgorithm import GeneticAlgorithm

if __name__ == '__main__':
    # gen_alg = GeneticAlgorithm('data/chromosome_20210306-120009_data.json', 500, 1)
    gen_alg = GeneticAlgorithm()
    gen_alg.run()


