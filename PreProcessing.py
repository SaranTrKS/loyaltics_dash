#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# In[10]:


table = pd.read_excel('Retail_Data.xlsx',sheet_name = [0,1,2])


# In[11]:


table.keys()


# In[14]:


trans = table[0]
cus_demo = table[1]
cus_add = table[2]


# In[16]:


type(trans)


# In[32]:


trans_dropdf = trans.dropna()
trans.info()


# In[31]:


trans.head()


# In[33]:


pwd()


# In[ ]:




