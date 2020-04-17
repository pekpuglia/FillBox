class Box:
    def __init__(self, sizes, vertex):
        self.sizes = sizes
        self.master_vertex = vertex #vertice mais próximo da origem
        self.vert_update()

    def vert_update(self):
        comb = [[x, y, z] for x in [0,1] for y in [0,1] for z in [0,1] ]
        self.vertexes = [[self.master_vertex[x] + comb[y][x] * self.sizes[x] for x in range(3)] for y in range(8)]

    def collide(self, box):
        for v in box.vertexes:
            if self.vertexes[0][0] <= v[0] <= self.vertexes[7][0] and \
               self.vertexes[0][1] <= v[1] <= self.vertexes[7][1] and \
               self.vertexes[0][2] <= v[2] <= self.vertexes[7][2]:
                return True
        for v in self.vertexes:
            if box.vertexes[0][0] <= v[0] <= box.vertexes[7][0] and \
               box.vertexes[0][1] <= v[1] <= box.vertexes[7][1] and \
               box.vertexes[0][2] <= v[2] <= box.vertexes[7][2]:
                return True
        return False
    
    def place(self, box, flag):
        #flag decide em qual face será
        #age na self
        if flag == 0:
            self.master_vertex = [box.master_vertex[0] + box.sizes[0], box.master_vertex[1], box.master_vertex[2]]
        elif flag == 1:
            self.master_vertex = [box.master_vertex[0], box.master_vertex[1] + box.sizes[1], box.master_vertex[2]]
        elif flag == 2:
            self.master_vertex = [box.master_vertex[0], box.master_vertex[1], box.master_vertex[2] +box.sizes[2]]
        self.vert_update() 

placed_boxes = []

def try_place(boxes, box):
    dx, dy, dz = box[0]/100, box[1]/100, box[2]/100
    for b in boxes:
        placed_boxes.append(b)
        collided = False
        for other in placed_boxes:
            if other == b:
                continue
            if  (b.collide(other)):
                collided = True
                break
        while collided:
            #caso em que realmente não cabem todas na caixa????
            if (b.master_vertex[0]+b.sizes[0]<box[0]):
                b.master_vertex[0] +=dx
                b.master_vertex[0] = round(b.master_vertex[0], 2)
            else:
                b.master_vertex[0] = 0
                if (b.master_vertex[1]+b.sizes[1]<box[1]):
                    b.master_vertex[1] += dy
                    b.master_vertex[1] = round(b.master_vertex[1], 2)

                else:
                    b.master_vertex[1] = 0
                    if (b.master_vertex[2]+b.sizes[2]<box[2]):
                        b.master_vertex[2] += dz
                        b.master_vertex[2] = round(b.master_vertex[2], 2)

            b.vert_update()
            collided = False
            for other in placed_boxes:
                if other == b:
                    continue
                if  (b.collide(other)):
                    collided = True
                    break
    #se nenhuma colide, checar se estão todas na caixa
    for b in boxes:
        for v in b.vertexes:
            if v[0] > box[0] or v[1] > box[1] or v[2] > box[2]:
                return [] #erro
    return boxes
            

def fill (box, *boxes):
    """Tenta preencher box com boxes.
    Cada argumento é um vetor 3D com as dimensões da caixa."""
    
    vol = 0
    box_list = []
    for b in boxes:
        vol += b[0]*b[1]*b[2]
        box_list.append(Box(b, [0,0,0]))
    if vol >= box[0]*box[1]*box[2]:
        print("Impossível")
        return
    boxes = try_place(box_list, box)
    if boxes == []:
        print("Impossível")
        return
    else:
        for b in boxes:
            print(b.master_vertex, b.sizes)            

