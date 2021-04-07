import random
import pygame
import neat
import os
from game import Head,Game,draw_all,BOARD_BLOCKS_X,BLOCK_SIZE,BOARD_BLOCKS_Y


# CONSTANTS
SCREEN = None
# 1 fitness point -> 100 points
MAX_TURNS = 200
FOOD_POINTS = 300
DEATH_POINTS = -500
STARTING_POINTS = 1000
FOOD_IN_VISION = 50
MOVE_POINTS = -1
OUTPUT_THRESHOLD = 0.6


def run(config_f):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_f)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 100)

    print('Best: {!s}'.format(winner))


def eval_genomes(genomes, config):
    SCREEN.fill((100, 100, 100))
    gen = 0
    gen += 1

    nets = []
    gens = []
    players = []

    tmp = 0
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        game_tmp = Game(BOARD_BLOCKS_X * BLOCK_SIZE, BOARD_BLOCKS_Y*BLOCK_SIZE,tmp)
        players.append(Head(
            random.randrange(BOARD_BLOCKS_X//4,BOARD_BLOCKS_X//4 * 3)*BLOCK_SIZE,
            random.randrange(BOARD_BLOCKS_Y//4,BOARD_BLOCKS_Y//4 * 3)*BLOCK_SIZE,
            game_tmp
        ))
        gens.append(genome)
        tmp += 1

    clock = pygame.time.Clock()
    run = True
    while run and len(players) > 0:

        clock.tick(300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        for x, player in enumerate(players):
            player.points += MOVE_POINTS
            player.move()
            player.alive_turns += 1
            player.hunger -= 1

            outputs = nets[players.index(player)].activate(player.checkVision3())
            #print(outputs)

            '''if outputs[0] > OUTPUT_THRESHOLD:
                player.turn_left()
            elif outputs[1] > OUTPUT_THRESHOLD:
                player.turn_right()
            '''
            turn = outputs.index(max(outputs))
            #print(outputs[outputs.index(max(outputs))])
            if turn == 0:
                pass
            if turn == 1:
                player.turn_left()
            if turn == 2:
                player.turn_right()

        for player in players:
            if player.collideCheck(player.posX,player.posY) or player.hunger <= 0:
                player.points += DEATH_POINTS
                gens[players.index(player)].fitness = player.points/100
                nets.pop(players.index(player))
                gens.pop(players.index(player))
                players.pop(players.index(player))

            if player.food_collect():
                player.points += FOOD_POINTS

            if player.alive_turns >= MAX_TURNS:
                gens[players.index(player)].fitness = player.points/100
                nets.pop(players.index(player))
                gens.pop(players.index(player))
                players.pop(players.index(player))

            draw_all(player.game, player,SCREEN)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
