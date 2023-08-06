from examples.think_bayes.make_data import make_cookies_observations
from probability.discrete.joint import Joint
from pgmpy.factors.discrete import JointProbabilityDistribution as JPD


# 1.3 The cookie problem
# ----------------------

cookie_data = make_cookies_observations()
cookies = Joint.from_observations(cookie_data)

p__vanilla__bowl_1 = cookies.conditional(bowl='bowl 1').p(flavor='vanilla')
print(f'p(vanilla | bowl 1) = {p__vanilla__bowl_1}')


# 1.4 Bayes's theorem
# -------------------

p__vanilla = cookies.p(flavor='vanilla')
print(f'p(vanilla) = {p__vanilla}')

p__bowl = Joint.from_dict({'bowl 1': 0.5, 'bowl 2': 0.5},
                          variables=['bowl'])
p__bowl_1 = p__bowl.p(bowl='bowl 1')
print(f'p(bowl 1) = {p__bowl_1}')

p__bowl_1__vanilla = p__bowl_1 * p__vanilla__bowl_1 / p__vanilla
print(f'p(bowl 1 | vanilla)'
      f' = {p__bowl_1} * {p__vanilla__bowl_1} / {p__vanilla}'
      f' = {p__bowl_1__vanilla}')

p__bowl_1__vanilla = cookies.conditional(flavor='vanilla').p(bowl='bowl 1')
print(f'p(bowl 1 | vanilla) ={p__bowl_1__vanilla}')


# 1.5 The diachronic interpretation
# =================================

p__bowl_2 = p__bowl.p(bowl='bowl 2')
p__vanilla__bowl_2 = cookies.conditional(bowl='bowl 2').p(flavor='vanilla')

p__vanilla = p__bowl_1 * p__vanilla__bowl_1 + p__bowl_2 * p__vanilla__bowl_2
print(f'p(vanilla) = '
      f'{p__bowl_1} * {p__vanilla__bowl_1} + '
      f'{p__bowl_2} * {p__vanilla__bowl_2} = '
      f'{p__vanilla}')


# 1.6 The M & M problem
# =====================

mix_1994 = Joint.from_dict({
    'brown': 0.3, 'yellow': 0.2, 'red': 0.2,
    'green': 0.1, 'orange': 0.1, 'tan': 0.1
}, variables='color')
mix_1996 = Joint.from_dict({
    'blue': 0.24, 'green': 0.2, 'orange': 0.16,
    'yellow': 0.14, 'red': 0.13, 'brown': 0.13
}, variables='color')

bag = Joint.from_dict({1994: 0.5, 1996: 0.5}, variables='bag')

p__yellow__1994 = mix_1994.p(color='yellow')
p__yellow__1996 = mix_1996.p(color='yellow')
p__green__1994 = mix_1994.p(color='green')
p__green__1996 = mix_1996.p(color='green')

likelihood_a = p__yellow__1994 * p__green__1996
likelihood_b = p__yellow__1996 * p__green__1994

prior_likelihood_a = bag.p(bag=1994) * likelihood_a
prior_likelihood_b = bag.p(bag=1996) * likelihood_b

normalization = prior_likelihood_a + prior_likelihood_b

print(prior_likelihood_a / normalization)
print(prior_likelihood_b / normalization)


# 1.7 The Monty Hall problem
# ==========================






# ===============================

jpd0 = JPD(
    variables=['bowl'],
    cardinality=[2],
    values=[0.4, 0.6]
)
jpd1 = JPD(
    variables=['bowl', 'flavor'],
    cardinality=[2, 2],
    values=[.1, .2, .3, .4]
)
jpd2 = jpd0 * jpd1
jpd2.normalize()
print(jpd0)
print(jpd1)
print(jpd2)


