import matplotlib.pyplot as plt
import binomialtree_cv

# option price of twitter with constant volatility
twitter_sd = 0.40
twitter_sigma = []
for i in range(16):
    twitter_sigma.append(twitter_sd)

test = binomial_tree(16,56,twitter_sigma,0.026,40,45,CallOption=True)
test.option_value()


# option price of twitter with different expiration time and constant volatility

twitter_call_list = []

for i in range(1,17):
    x = binomial_tree(16,5*i,twitter_sigma,0.024,39.91,43,CallOption=True)
    twitter_call_list.append(x.option_value())
    
# option price of twitter with different expiration time and different volatility

twitter_call_list_2 = []
twitter_sigma_2 = []

y = twitter_sd
for i in range(16):
    y -= 0.01
    twitter_sigma_2.append(y)
    
for i in range(1,17):
    x = binomial_tree(16,5*i,twitter_sigma_2,0.024,39.91,43,CallOption=True)
    twitter_call_list_2.append(x.option_value())


plt.plot(np.arange(16,0,-1), twitter_call_list, 'ro',np.arange(16,0,-1),twitter_call_list_2,'bo')
plt.gca().legend(("Constant Volatility", "Changing Volatility"))
plt.show()
