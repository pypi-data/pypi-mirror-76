
# coding: utf-8

# # Plotting Evolution of Ages pyramid over years

# In[6]:


# Import necessary packages
from pop_projection import Effectifs as eff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[7]:


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


# In[8]:


# Path for input data
path ="./pop_projection/data/"


# In[9]:


# Loading data
employees = pd.read_csv(path + "employees.csv",sep=";", decimal = ",")
spouses = pd.read_csv(path + "spouses.csv",sep=";", decimal = ",")
children = pd.read_csv(path + "children.csv",sep=";", decimal = ",")


# In[10]:


# Diplay some data
print('Employees :')
print(employees.head(10))
print('Spouses :')
print(spouses.head(10))
print('Children :')
print(children.head(10))


# In[11]:


# Projection of population
# Number of years to project
MAX_ANNEES = 100

# Projection
numbers_ = eff.projectNumbers(employees, spouses, children, 'TV 88-90', MAX_ANNEES, law_replacement_ = law_replacement1)

# Getting individual numbers for employees (lives, deaths, resegnations, types)
ind_emp_numbers = eff.individual_employees_numbers(numbers_[0])

# Getting lives numbers of employees
employees_proj = ind_emp_numbers[0]

# Displaying some lines of lives numbers of employees
print(employees_proj.head(10))


# In[12]:


# Title of individual plots
year = 'year_'

# Size of plot
plt.rcParams['figure.figsize'] = [10, 15]

for i in range(1, MAX_ANNEES//10):
    
    emp_grouped = employees_proj.groupby(['age','sex'], as_index=False)[year+str((i-1)*10)].sum()
    
    max_age = 55 # 101
    
    min_age = 19
    
    #update colum age to be age at year (i-1)*10
    emp_grouped['age'] = emp_grouped['age'] - MAX_ANNEES + (i-1)*10
    
    emp_grouped = emp_grouped.loc[(emp_grouped['age'] < max_age) & (emp_grouped['age'] > min_age)]
    
    table = pd.pivot_table(emp_grouped, values=year+str((i-1)*10), index=['age'],  columns=['sex'], aggfunc=np.sum)
    
    table = table.fillna(0)
    
    #calculate percentage
    if 'male' in list(table.columns):
        table['male'] = table['male']/np.sum(table['male'])
    if 'female' in list(table.columns):
        table['female'] = table['female']/np.sum(table['female'])
    
    if 'female' in list(table.columns):
        table['female'] = table['female'] * (-1)
    
    plt.subplot(4 , 4, i)
    plt.subplots_adjust(hspace = 0.5)
    plt.xlim(-0.05,0.05)
    plt.title('Year ' + str((i-1)*10))
    
    if 'male' in list(table.columns):
        values = [0] * (max_age - min_age - 1)
        for i in range(len(table['male'])):
            values[table.index[i] - min_age - 1] = table.iloc[i]['male']
        p_male = plt.barh(list(range(min_age + 1, max_age)), values, color = (149/255,125/255,98/255) )
    
    if 'female' in list(table.columns):
        for i in range(len(table['female'])):
            values[table.index[i] - min_age - 1] = table.iloc[i]['female']
        p_female = plt.barh(list(range(min_age + 1, max_age)), values, color = (0/255,128/255,0/255))

    plt.figlegend((p_male[0], p_female[0]), ('Men', 'Women'), loc = 'lower center')
    plt.suptitle('Evolution of Ages Pyramid')

plt.show()

