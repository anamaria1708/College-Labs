from Programs.GeneticAlgorithm import GeneticAlgorithm

from Tasks.TaskFunctions import *

from copy import copy
import cProfile



def TaskOne():
  problem_bounds = (-50,150)
  max_evals = 10000
  desired_goal_value = (0.1)**6
  divergence_at = 1000

  iterations = 11
  results = []
  for i in range(iterations):
    # GA = GeneticAlgorithm(goal_function=f1, dimensions=2, problem_bounds=problem_bounds,
                          # fitness_bounds=(0,100), population_size=100, display="float", precision=8, p_of_mutation=0.01, 
                          # max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)
    
    # GA = GeneticAlgorithm(goal_function=f3, dimensions=5, problem_bounds=problem_bounds,
                          # fitness_bounds=(0,100), population_size=4, display="float", precision=8, p_of_mutation=0.01, 
                          # max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)
    
    # GA = GeneticAlgorithm(goal_function=f6, dimensions=2, problem_bounds=problem_bounds,
                                # fitness_bounds=(0,100), population_size=100, display="binary", precision=4, p_of_mutation=0.01, 
                                # max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)
    
    GA = GeneticAlgorithm(goal_function=f7, dimensions=2, problem_bounds=problem_bounds,
                                fitness_bounds=(0,100), population_size=100, display="float", precision=0, p_of_mutation=0.01, 
                                max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)
    
    point, goal_value = GA.SolveProblem()
    results.append((goal_value, point))

  results = SortGoalAndPoint(results)
  count = CountSuccesses(results, desired_goal_value)
  PrintResults(results, count, iterations)
  
def TaskTwo():
  problem_bounds = (-50,150)
  max_evals = 10000
  desired_goal_value = (0.1)**6
  divergence_at = 1000
  
  iterations = 3
  dimensions = [1,3,6,10]
  for d in dimensions:
    results = []
    for i in range(iterations):
      GA = GeneticAlgorithm(goal_function=f6, dimensions=d, problem_bounds=problem_bounds,
                                    fitness_bounds=(0,100), population_size=20, display="binary", precision=4, p_of_mutation=0.01, 
                                    max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)
        
      # GA = GeneticAlgorithm(goal_function=f7, dimensions=d, problem_bounds=problem_bounds,
                                  # fitness_bounds=(0,100), population_size=20, display="binary", precision=4, p_of_mutation=0.01, 
                                  # max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)

      point, goal_value = GA.SolveProblem()
      results.append((goal_value, point))

    results = SortGoalAndPoint(results)
    count = CountSuccesses(results, desired_goal_value)
    PrintResults(results, count, iterations)
  
def TaskThree():
  problem_bounds = (-50,150)
  max_evals = 100000
  desired_goal_value = (0.1)**6
  divergence_at = 1000
  
  binary_display = False
  d = 6
  
  iterations = 11
  results = []
  for i in range(iterations):
    
    GA = GeneticAlgorithm(goal_function=f6, dimensions=d, problem_bounds=problem_bounds,
                                fitness_bounds=(0,100), population_size=20, binary_display=binary_display, precision=4, p_of_mutation=0.01, 
                                max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)
                                
    # GA = GeneticAlgorithm(goal_function=f7, dimensions=d, problem_bounds=problem_bounds,
                                # fitness_bounds=(0,100), population_size=20, binary_display=binary_display, precision=4, p_of_mutation=0.01, 
                                # max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)
                                
    point, goal_value = GA.SolveProblem()
    results.append((goal_value, point))

  results = SortGoalAndPoint(results)
  count = CountSuccesses(results, desired_goal_value)
  PrintResults(results, count, iterations)
  
def TaskFour():
  problem_bounds = (-50,150)
  max_evals = 10000
  desired_goal_value = (0.1)**6
  divergence_at = 1000

  iterations = 11
  
  #population_values = [30, 50, 100, 200] #[30, 50, 100, 200]
  mutation_values = [0.01, 0.03, 0.06, 0.1] #[0.1, 0.3, 0.6, 0.9]
  #for pop_value in population_values:
  for mut_value in mutation_values:
    results = []
    for i in range(iterations):   
      GA = GeneticAlgorithm(goal_function=f6, dimensions=2, problem_bounds=problem_bounds,
                                  fitness_bounds=(0,100), population_size=100, display="binary", precision=4, p_of_mutation=mut_value, 
                                  max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)
      
      point, goal_value = GA.SolveProblem()
      results.append((goal_value, point))
      print goal_value

    results = SortGoalAndPoint(results)
    count = CountSuccesses(results, desired_goal_value)
    PrintResults(results, count, iterations)
  
def TaskFive():
  """
  The tournament size is set at k=3, but it can be increased for testing purposes within the algorithm.
  WARNING: always return the tournmanet size  after testing.
  """
  problem_bounds = (-50,150)
  max_evals = 10000
  desired_goal_value = (0.1)**6
  divergence_at = 1000

  iterations = 21
  results = []
  for i in range(iterations):
    GA = GeneticAlgorithm(goal_function=f6, dimensions=2, problem_bounds=problem_bounds,
                                fitness_bounds=(0,100), population_size=100, display="binary", precision=0, p_of_mutation=0.01, 
                                max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)

    point, goal_value = GA.SolveProblem()
    results.append((goal_value, point))
    print goal_value

  results = SortGoalAndPoint(results)
  count = CountSuccesses(results, desired_goal_value)
  PrintResults(results, count, iterations)
 
def SIAMHundredDigitChallenge():
  problem_bounds = (0,20)
  max_evals = 100000
  desired_goal_value = (-3.3068686473)
  divergence_at = 5000

  iterations = 501
  results = []
  for i in range(iterations):
    GA = GeneticAlgorithm(goal_function=SIAMf, dimensions=2, problem_bounds=problem_bounds,
                                fitness_bounds=(0,100), population_size=200, display="float", precision=0, p_of_mutation=0.01, 
                                max_evaluations=max_evals, reach_goal=desired_goal_value, no_improvement_limit=divergence_at)
    
    point, goal_value = GA.SolveProblem()
    results.append((goal_value, point))

  results = SortGoalAndPoint(results)
  count = CountSuccesses(results, desired_goal_value)
  PrintResults(results, count, iterations)
 
def ParamOpti():
  problem_bounds = (-50,150)
  max_evals = 10000
  desired_goal_value = (0.1)**6
  
  iterations = 21
  
  population_values = [30, 50, 100, 200] #[30, 50, 100, 200]
  mutation_values = [0.01,0.05] #[0.01,0.05,0.1,0.2,0.5]
  precision_values = [0,2,4,8,16]
  for opti_value in mutation_values:
    results = []
    for i in range(iterations):
      GA = GeneticAlgorithm(goal_function=f6, dimensions=2, problem_bounds=problem_bounds,
                            fitness_bounds=(0,100), population_size=50, display="binary", precision=8, p_of_mutation=opti_value, 
                            max_evaluations=max_evals, reach_goal=desired_goal_value)
      point, goal_value = GA.SolveProblem()
      results.append((goal_value, point))
  
  
    results = SortGoalAndPoint(results)
    count = CountSuccesses(results, desired_goal_value)
    PrintResults(results, count, iterations)
    print "optimization_value:",
    print opti_value
        
def SortGoalAndPoint(results):
  results = sorted(results, key=lambda result: result[0])
  return results
  
def CountSuccesses(results, desired_goal_value):
  count = 0
  for result in results:
    if result[0] < desired_goal_value:
      count += 1
      
  return count
  
def PrintResults(results, count, iterations):
  print "reached desired goal value:",
  print count
  print "median_goal_value:",
  print results[iterations/2][0]
  print "point:",
  print results[iterations/2][1]
  
  for i in range(len(results) / 5):
    print results[i]
  

#cProfile.run("ParamOpti()")
#TaskOne()
#TaskTwo()
#TaskThree()
#TaskFour()
SIAMHundredDigitChallenge()
#cProfile.run("TaskFive()")