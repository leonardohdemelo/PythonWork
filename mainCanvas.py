#Arquivo que manipula as ações sobre o canvas


import tkinter as tk
from functools import partial
import math
#-------***********-----------#
from mainAlgorithm import graphStructure as gS

class makeCanvas:
  #Variveis que pertencem a todos os nós
  node_list = list()
  node_number = 0
  size = 30
  def __init__(self, root ,canvas):
    self.root = root
    self.canvas = canvas
    self.graph = gS() 
    self.canvas.pack()
    self.canvas.bind("<Button-1>", self.draw_item)
    self.line_start = None

  def draw_item(self, event):
    x, y = event.x, event.y
    if(self.verify_pos(x,y)):
      bbox = (x-self.size, y-self.size, x+self.size, y+self.size)
      self.item = self.canvas.create_oval(*bbox, fill="blue", activefill="grey", tags = "node")
      elem_value = self.insert_node(self.item)
      text = self.canvas.create_text(x,y,fill = "white", font = "Times 20 bold", text=str(elem_value), tags = "text")
      self.canvas.tag_bind(text, '<Enter>', self.textFocus)
      self.canvas.tag_bind(text, '<Leave>', self.textUnfocus)
      self.line_start = None

  def set_size(self, valor): 
    self.size = valor

  def insert_node(self,c_item):
      i = 0
      if(self.node_number > 0):
        elem = self.node_list[i]
        while (elem != -1 and i < self.node_number-1):
          elem = self.node_list[i]
          i += 1
        
        i+= 1

        if i < self.node_number-1:
          self.node_list[i] = i
        else:
          self.node_list.append(c_item)
          self.node_number += 1
      else:
          self.node_list.append(c_item)
          self.node_number += 1

      self.graph.insertNode(i)

      return i

  def verify_pos(self, x, y):
    node = self.canvas.find_withtag(tk.CURRENT)

    if(node!=()):
      tag = self.canvas.itemcget(node, "tags").split(" ")[0]
      node = node[0]

      #assim ele pegara textos tambem
      if(tag=="text"):
        node=node-1

      #no caso de ser uma edge
      if(tag=="text" or tag=="node"):
        x0, y0, x1, y1 = self.canvas.coords(node)
      else:
        return True

      self.draw_Edge(node, x1, y1)
      return False

    return True

  def draw_Edge(self, node, x1, y1):
    if not self.line_start:
        self.line_start = (x1-self.size,y1-self.size,self.node_list.index(node))
        print(self.line_start)
    else:
      x_origin,y_origin,node_origin = self.line_start
      
      #tirando edge do node
      angle = math.atan((x1-self.size-x_origin)/(y1-self.size-y_origin))
      xoffset = self.size*math.sin(angle)
      yoffset = self.size*math.cos(angle)
      if(y1-self.size<y_origin):
        yoffset = -1*yoffset
        xoffset = -1*xoffset

      self.line_start=None
      line=(x_origin+xoffset,y_origin+yoffset,x1-self.size-xoffset,y1-self.size-yoffset)
      self.canvas.create_line(*line, fill = "black")
      self.graph.insertEdge((node_origin,self.node_list.index(node)))

  def textFocus(self, event):
    text = self.canvas.find_withtag(tk.CURRENT)
    if(text!=()):
      text=text[0]
      self.canvas.itemconfigure(text-1,fill="grey")
  
  def textUnfocus(self, event):
    text = self.canvas.find_withtag(tk.CURRENT)
    if(text!=()):
      text=text[0]
      self.canvas.itemconfigure(text-1,fill="blue")