import os
os.chdir("/home/branche/ML_TERM/gym-micropolis-ga/")
from mapPrinter import getMapImage, saveMapInts
os.chdir("/home/branche/ML_TERM/gym-micropolis-ga/")
from MicropolisControlScript import Quimby
import pickle


# Parameters
map_size = 30
chromosome_len = 100
steps = 39 # For 5 years of simulation
nb_generations = 20
eval = "last"
n_population = 50

# The next parameters are interesting to cross map :
crossover = ["switch", "split"]
mutation_rate = [0, 0.2, 0.5]
p_selection = [0.2]
couple_size = [2, 5]
# nb_splits = [1, 5]

# this program's specifics :
crossover = ["switch"]

savepath="saves/small_cross/"
filename=""

if not os.path.exists(savepath):
    os.makedirs(savepath)



for c in crossover:
    for mr in mutation_rate:
        for p in p_selection:
            for cs in couple_size:

                filename = "c_" + c + "-m_" + str(int(100 * mr)) + "-p_" + str(int(100 * p)) + "-cs_" + str(cs)
                print(filename)

                # Run the algorithm
                q = Quimby(map_w=map_size, map_h=map_size, chromosome_len=200, n_population=n_population,
                           n_steps_evaluation=steps)
                q.ga(nb_generations=nb_generations, mutation_rate=mr, p_selection=p, couple_size=cs, crossover=c,
                     eval=eval)

                # Best score of that Quimby
                score = q.pop_progression[-1]
                filename = filename + "-bestScore_" + str(score)

                # Save the quimby class
                pickle.dump(q, open(savepath + filename + ".obj", 'wb'))

                # Generate all the maps and save them
                for cityindex in range(len(q.genomes)):

                    cityname = filename + "-city_" + str(cityindex) + "-score_" + str(q.populations[cityindex])

                    m = q.build_city(city=q.genomes[cityindex], display=False)
                    # Save PNG image
                    getMapImage(m.getTileMap()).save(savepath + cityname + ".png", "PNG")
                    # Save numpy matrix of ints
                    saveMapInts(m.getTileMap(), savepath + cityname + ".npy")

                    m.close()


quimby_name = "saves/gan_cross/c_split-m_0-p_20-cs_2-bestScore_5120.obj"
cityindex =
q = pickle.load(open('saves/s_test_savescore.obj', 'rb'))
city = q.genomes[np.argmax(q.populations)]
m = q.build_city(city=q.genomes[cityindex], display=False)
# Save PNG image
getMapImage(m.getTileMap()).save(savepath + cityname + ".png", "PNG")

showMap(m)

m.close()
