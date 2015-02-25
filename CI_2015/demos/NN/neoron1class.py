# This code does  the same as the neuron1.py
# But we have encapsulated the neuron as a class.




class Neuron:
  
  def __init__(self, n_in):
      """
      create a neuron with n_in inputs.
      remember to set the weights before  calling fire.
      """
      self.n_in = n_in

  def fire(self, input):
      """
      Activate the neuron using the given input
      return 0 or 1  (fire or not)
      """
      sum = self.weights[self.n_in]
      for x, w in zip(input, self.weights):
        sum += x * w
        
      if sum > 0.0:
            return 1.0
      else:
            return 0.0
    
  def set_weights(self, weights):
      """
      Set the weights of the neuron
      """
      self.weights = weights


# Create a neuron
neuron = Neuron(3)

# Set it's weights
neuron.set_weights([1., -2., 1., 1.0])

print " X1 X2 X3    OUTPUT"
for x1 in range(2):
    for x2 in range(2):
        for x3 in range(2):
            input = [x1, x2, x3]
            output = neuron.fire(input)
            print " %2.0f %2.0f %2.0f  | %2.0f  " % (x1, x2, x3, output)
            

