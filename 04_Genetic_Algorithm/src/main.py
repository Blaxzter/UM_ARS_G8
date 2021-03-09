import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from genetic.GeneticAlgorithm import GeneticAlgorithm

if __name__ == '__main__':
    # gen_alg = GeneticAlgorithm(
    #     load='data/chromosome_20210306-120009_data.json',
    #     generation=-1,
    #     show_best=1,
    #     # room = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    #     # room = [6, 6, 6, 6, 6, 6, 6, 6, 6]
    #     room = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # )
    # gen_alg.run()

    # gen_alg = GeneticAlgorithm(
    #     load='data/chromosome_20210306-120009_data.json',
    #     generation=697,
    #     show_best=1,
    #     # room = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    #     room = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # )
    # gen_alg.run()


    # gen_alg = GeneticAlgorithm(
    #     load='data/154_Avg_over_8_rooms.json',
    #     generation=-1,
    #     show_best=1,
    #     room = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    #     # room = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # )
    # gen_alg.run()

    gen_alg = GeneticAlgorithm()
    gen_alg.run()

    # for i in range(1, 20):
    #     gen_alg = GeneticAlgorithm(file_name = f'run_{i}.json')
    #     gen_alg.run()
