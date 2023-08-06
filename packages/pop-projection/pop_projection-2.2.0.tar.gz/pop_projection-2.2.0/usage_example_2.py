
# coding: utf-8

# # Ages pyramid at year 50 for different mortality tables

# In[2]:


# Import necessary packages
from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[3]:


# Define law of replacement
def law_replacement1(departures_, year_):
    
    '''
        assumes departures_ is a dic storing number of departures by group of the year year_
        returns a list of dics having keys : key, number and data
        
    '''
    def nouveaux(g_):
        structure_nouveaux = {'1':[25,25,0.8],'2':[25,25,0.8],'3':[25,25,0.6],'4':[29,29,0.6],'5':[28,28,0.5,],
        '6':[28,28,0.5],'7':[33,33,0.5],'8':[38,38,0.5],'9':[38,38,0.5],'10':[47,47,0.5],'11':[49,49,0.5]}

        if str(g_) in structure_nouveaux:
            return structure_nouveaux[str(g_)]
        else:
            return [30, 30, 1.0]

    def taux_rempl(y, g_ = '0'):
        if y <= 3 :
            if str(g_) in ['1','2','3','5','6','7']:
                return 0.64
            else:
                return 1
        else:
            return 1

    new_employees = []

    for g in departures_:
        # add a male
        if nouveaux(g)[2] > 0:
            temp = {'key':'male_groupe_' + str(g) + 'year_' + str(year_), 
            'number':nouveaux(g)[2]*departures_[g]*taux_rempl(year_, g),'data':['active', 'male', 'not married', nouveaux(g)[0], year_,g,'01/01/'+str((2018+year_+1)),'31/12/'+str((2018+year_-nouveaux(g)[0]))]}
            new_employees.append(temp)

        # add a female
        if nouveaux(g)[2] < 1:
            temp = {'key':'female_groupe_' + str(g) + 'year_' + str(year_), 
            'number':(1-nouveaux(g)[2])*departures_[g]*taux_rempl(year_, g),'data':['active', 'female', 'not married', nouveaux(g)[1], year_,g,'01/01/'+str((2018+year_+1)),'31/12/'+str((2018+year_-nouveaux(g)[1]))]}
            new_employees.append(temp)
    
    return new_employees


# In[4]:


# Define law of marriage
def law_mar1(age, sex, type):
    """
    Return the probability of getting maried  during the following year at a given age for a given sex

    """
    if sex == 'male':
        if type=='active':
            if age >= 25 and age <= 54:
                return 0.1
            else :
                return 0
        else:
            return 0
    
    if sex == 'female':
        if type=='active':
            if age >= 25 and age <= 54:
                return 0.15
            else :
                return 0
        else:
            return 0


# In[5]:


# Path for input data
path ="./pop_projection/data/"


# In[6]:


# Number of years to project
MAX_ANNEES = 100


# In[7]:


# Loading data
employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")


# In[8]:


# Diplay some data
print('Employees :')
print(employees.head(10))
print('Spouses :')
print(spouses.head(10))
print('Children :')
print(children.head(10))


# In[11]:


# Mortality tables to use for plots
tables = ['TD 73-77', 'TD 90-92', 'TV 88-90']


# In[14]:


# some initialisations
year_ = 51
plot_num = 1
min_age_ = 19
max_age_ = 100
color_males = (149/255,125/255,98/255) 
color_females = (0/255,128/255,0/255)

for t in tables:

    # Projection of population
    numbers_ = eff.projectNumbers(employees, spouses, children, t, MAX_ANNEES, law_replacement_ = law_replacement1, law_marriage_=law_mar1)

    # Pyramid of spouses
    ind_spo_numbers = eff.individual_spouses_numbers(numbers_[1])
    spouses_proj = ind_spo_numbers[0]
    
    emp_grouped = spouses_proj.groupby(['age','sex'], as_index=False)['year_'+str((year_-1))].sum()
        
    #update colum age to be age at year (year_-1)
    emp_grouped['age'] = emp_grouped['age'] - MAX_ANNEES + (year_-1)
    
    emp_grouped = emp_grouped.loc[(emp_grouped['age'] < max_age_) & (emp_grouped['age'] > min_age_)]
    
    table = pd.pivot_table(emp_grouped, values='year_'+str((year_-1)), index=['age'],  columns=['sex'], aggfunc=np.sum)
    
    table = table.fillna(0)
    
    #calculate percentage
    if 'male' in list(table.columns):
        table['male'] = table['male']/np.sum(table['male'])
    if 'female' in list(table.columns):
        table['female'] = table['female']/np.sum(table['female'])
    
    if 'female' in list(table.columns):
        table['female'] = table['female'] * (-1)
    
    plt.subplot(len(tables) , 1, plot_num)
    plt.subplots_adjust(hspace = 0.5)
    plt.xlim(-0.05,0.05)
    plt.title(t)
    
    if 'male' in list(table.columns):
        values = [0] * (max_age_ - min_age_ - 1)
        for i in range(len(table['male'])):
            values[table.index[i] - min_age_ - 1] = table.iloc[i]['male']
        p_male = plt.barh(list(range(min_age_ + 1, max_age_)), values, color = color_males )
    
    if 'female' in list(table.columns):
        for i in range(len(table['female'])):
            values[table.index[i] - min_age_ - 1] = table.iloc[i]['female']
        p_female = plt.barh(list(range(min_age_ + 1, max_age_)), values, color = color_females)
    plot_num += 1
    plt.figlegend((p_male[0], p_female[0]), ('Men', 'Women'), loc = 'lower center')

plt.suptitle('Spouses Ages Pyramid by mortality table')
plt.show()

