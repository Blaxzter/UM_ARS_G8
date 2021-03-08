import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from genetic.GeneticAlgorithm import GeneticAlgorithm

if __name__ == '__main__':
    # gen_alg = GeneticAlgorithm(
    #     load='data/chromosome_20210308-004004_data.json',
    #     generation=0,
    #     show_best=1,
    #     room = [0]
    # )

    for i in range(20):
        gen_alg = GeneticAlgorithm(file_name = f'run_{i}.json')
        gen_alg.run()
