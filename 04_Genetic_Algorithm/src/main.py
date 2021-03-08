import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from genetic.GeneticAlgorithm import GeneticAlgorithm

if __name__ == '__main__':
    gen_alg = GeneticAlgorithm(
        load='data/154_Avg_over_8_rooms.json',
        generation=-1,
        show_best=1,
        room = [0, 0, 0, 0, 0]
    )
    gen_alg.run()

    #
    # for i in range(20):
    #     gen_alg = GeneticAlgorithm(file_name = f'run_{i}.json')
    #     gen_alg.run()
