import random
import math

# Koordináták
START = (0, 0)
GOAL = (76, 89)
GRID_SIZE = 100

# Irányok: fel, le, balra, jobbra
DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def is_valid(pos):
    """Ellenőrzi, hogy a pozíció a határon belül van-e"""
    return 0 <= pos[0] < GRID_SIZE and 0 <= pos[1] < GRID_SIZE


def distance(pos1, pos2):
    """Euklideszi távolság két pont között"""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def random_walk():
    """Random Walk algoritmus implementálása"""
    print("=== RANDOM WALK ALGORITMUS ===")
    path = [START]
    current = START
    steps = 0
    max_steps = 100000  # Biztonsági korlát

    while current != GOAL and steps < max_steps:
        # Véletlenszerű irány választása
        direction = random.choice(DIRECTIONS)
        new_pos = (current[0] + direction[0], current[1] + direction[1])

        # Ellenőrzés, hogy érvényes-e a pozíció
        if is_valid(new_pos):
            current = new_pos
            path.append(current)
            steps += 1

    if current == GOAL:
        print(f"Cél elérve {steps} lépésben!")
    else:
        print(f"Nem sikerült elérni a célt {max_steps} lépésben")

    return path, steps


class Individual:
    """Egy egyén a genetikus algoritmusban"""

    def __init__(self, gene_length=500):
        self.genes = [random.choice(DIRECTIONS) for _ in range(gene_length)]
        self.fitness = 0
        self.path = []

    def calculate_fitness(self):
        """Fitness érték számítása"""
        current = START
        self.path = [current]

        for gene in self.genes:
            new_pos = (current[0] + gene[0], current[1] + gene[1])
            if is_valid(new_pos):
                current = new_pos
                self.path.append(current)
                if current == GOAL:
                    break

        # Fitness: minél közelebb van a célhoz, annál jobb
        dist = distance(current, GOAL)
        self.fitness = 1 / (dist + 1)

        # Bónusz, ha elérte a célt
        if current == GOAL:
            self.fitness += 10

        return self.fitness


def tournament_selection(population, tournament_size=5):
    """Tournament selection"""
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=lambda ind: ind.fitness)


def crossover(parent1, parent2):
    """Egypontos keresztezés"""
    if random.random() < 0.8:  # 80% keresztezési valószínűség
        child1 = Individual(len(parent1.genes))
        child2 = Individual(len(parent2.genes))

        for i in range(len(parent1.genes)):
            if random.random() < 0.5:
                child1.genes[i] = parent1.genes[i]
                child2.genes[i] = parent2.genes[i]
            else:
                child1.genes[i] = parent2.genes[i]
                child2.genes[i] = parent1.genes[i]

        return child1, child2
    else:
        return parent1, parent2


def mutate(individual, mutation_rate=0.2):
    """Mutáció: véletlenszerű génváltoztatás"""
    for i in range(len(individual.genes)):
        if random.random() < mutation_rate:
            individual.genes[i] = random.choice(DIRECTIONS)


def genetic_algorithm(population_size=100, generations=500, gene_length=500):
    """Genetikus algoritmus implementálása"""
    print("\n=== GENETIKUS ALGORITMUS ===")

    # Kezdeti populáció létrehozása
    population = [Individual(gene_length) for _ in range(population_size)]

    best_individual = None
    best_fitness_history = []

    for generation in range(generations):
        # Fitness számítása minden egyedre
        for individual in population:
            individual.calculate_fitness()

        # Legjobb egyed kiválasztása
        population.sort(key=lambda ind: ind.fitness, reverse=True)
        best_individual = population[0]
        best_fitness_history.append(best_individual.fitness)

        print(f"Generáció {generation + 1}/{generations} - "
              f"Legjobb fitness: {best_individual.fitness:.4f} - "
              f"Lépések: {len(best_individual.path)}")

        # Ha elértük a célt, leállhatunk
        if best_individual.path[-1] == GOAL:
            print(f"Cél elérve a {generation + 1}. generációban!")
            break

        # Új populáció létrehozása
        new_population = []

        # Elitizmus: legjobb 10% megtartása
        elite_size = population_size // 10
        new_population.extend(population[:elite_size])

        # Új egyedek létrehozása
        while len(new_population) < population_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            child1, child2 = crossover(parent1, parent2)

            mutate(child1)
            mutate(child2)

            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)

        population = new_population

    return best_individual, best_fitness_history


def print_path_stats(path, title, steps):
    """Útvonal statisztikák kiírása"""
    print(f"\n{title}")
    print("-" * 50)
    print(f"Lépések száma: {steps}")
    print(f"Kezdőpont: {START}")
    print(f"Végpont: {path[-1]}")
    print(f"Célpont: {GOAL}")
    print(f"Cél elérve: {'Igen' if path[-1] == GOAL else 'Nem'}")
    if path[-1] != GOAL:
        print(f"Távolság a céltól: {distance(path[-1], GOAL):.2f}")


def main():
    """Fő program"""
    print("=" * 50)
    print("ÚTKERESÉSI ALGORITMUSOK ÖSSZEHASONLÍTÁSA")
    print("=" * 50)
    print(f"Start: {START}")
    print(f"Cél: {GOAL}")
    print(f"Rács mérete: {GRID_SIZE} × {GRID_SIZE}")
    print("=" * 50)

    # Random Walk
    rw_path, rw_steps = random_walk()
    print_path_stats(rw_path, "RANDOM WALK EREDMÉNYEK", rw_steps)

    # Genetikus Algoritmus
    best_individual, fitness_history = genetic_algorithm(
        population_size=100,
        generations=500,
        gene_length=500
    )

    ga_path = best_individual.path
    ga_steps = len(ga_path)

    print_path_stats(ga_path, "GENETIKUS ALGORITMUS EREDMÉNYEK", ga_steps)

    # Összehasonlítás
    print("\n" + "=" * 50)
    print("ÖSSZEHASONLÍTÁS")
    print("=" * 50)
    print(f"Random Walk lépések: {rw_steps}")
    print(f"Genetikus Algoritmus lépések: {ga_steps}")
    if rw_steps > ga_steps:
        print(f"Különbség: {rw_steps - ga_steps} lépés")
        print(f"Genetikus algoritmus {(rw_steps / ga_steps):.2f}x hatékonyabb")
    else:
        print(f"Különbség: {ga_steps - rw_steps} lépés")
        print(f"Random Walk volt hatékonyabb ezúttal")
    print("=" * 50)


if __name__ == "__main__":
    main()