
# coding: utf-8

# In[64]:


from graph_tool.all import *
import random
from IPython.display import Image

g = random_graph(30, lambda: random.randint(2,3), False)
print (g)
graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=25, output_size=(500, 500), output="image.png")
Image(filename='image.png') 


# In[65]:


clust = local_clustering(g, undirected = False)
print(vertex_average(g, clust))


# In[66]:


print(global_clustering(g))


# In[67]:


clusts = extended_clustering(g, max_depth=5)
for i in range(0, 5):
    print(vertex_average(g, clusts[i]))


# In[68]:


state = minimize_nested_blockmodel_dl(g, 2, 4, deg_corr=True, overlap=True)
state.draw(output="clustered.png")
Image(filename='clustered.png') 

