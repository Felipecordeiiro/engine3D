import numpy as np

class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVBO(ctx)
        self.vbos['sphere'] = SphereVBO(ctx)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]


class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attribs: list = None

    def get_vertex_data(self): ...

    # Vertex data to GPU memory
    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        self.vbo.release()


class CubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1),]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   ( 0,-1, 0) * 6,]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data

class SphereVBO(BaseVBO):
    def __init__(self, ctx, latitude_bands=20, longitude_bands=20):
        self.latitude_bands = latitude_bands
        self.longitude_bands = longitude_bands
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
    
    def get_vertex_data(self):
        vertices, normals, tex_coords, indices = self.generate_sphere()
        
        vertex_data = np.array([vertices[i] for i in indices], dtype='f4')
        normal_data = np.array([normals[i] for i in indices], dtype='f4')
        tex_coord_data = np.array([tex_coords[i] for i in indices], dtype='f4')
        
        vertex_data = np.hstack([tex_coord_data, normal_data, vertex_data])
        return vertex_data
    
    def generate_sphere(self):
        vertices = []
        normals = []
        tex_coords = []
        indices = []
        
        for lat in range(self.latitude_bands + 1):
            theta = lat * np.pi / self.latitude_bands
            sin_theta = np.sin(theta)
            cos_theta = np.cos(theta)
            
            for lon in range(self.longitude_bands + 1):
                phi = lon * 2 * np.pi / self.longitude_bands
                sin_phi = np.sin(phi)
                cos_phi = np.cos(phi)
                
                x = cos_phi * sin_theta
                y = cos_theta
                z = sin_phi * sin_theta
                
                u = 1 - (lon / self.longitude_bands)
                v = 1 - (lat / self.latitude_bands)
                
                vertices.append((x, y, z))
                normals.append((x, y, z))
                tex_coords.append((u, v))
        
        for lat in range(self.latitude_bands):
            for lon in range(self.longitude_bands):
                first = lat * (self.longitude_bands + 1) + lon
                second = first + self.longitude_bands + 1
                
                indices.append(first)
                indices.append(second)
                indices.append(first + 1)
                
                indices.append(second)
                indices.append(second + 1)
                indices.append(first + 1)
        
        return vertices, normals, tex_coords, indices