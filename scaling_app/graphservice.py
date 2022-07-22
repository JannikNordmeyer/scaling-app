import wx


class GraphService:

    def __init__(self, frame, datastorage):
        self.frame = frame
        self.datastorage = datastorage

    def draw_lattice(self):

        maxwidth = 1
        maxdepth = 1

        allnodes = dict()

        for node in self.datastorage.context['positions']:
            for name, coords in node.items():
                allnodes[name] = coords
                if abs(coords[0]) > maxwidth:
                    maxwidth = abs(coords[0])
                if abs(coords[1]) > maxdepth:
                    maxdepth = abs(coords[1])

        dc = wx.ClientDC(self.frame.panelLeft)
        width, height = self.frame.panelLeft.GetSize()

        for edges in self.datastorage.context['edges']:
            for origin in edges:
                for target in edges[origin]:
                    dc.DrawLine(allnodes[origin][0] * (width / (2 * maxwidth)) + width / 2,
                                allnodes[origin][1] * (height / maxdepth) * 0.9 + height * 0.04,
                                allnodes[target][0] * (width / (2 * maxwidth)) + width / 2,
                                allnodes[target][1] * (height / maxdepth) * 0.9 + height * 0.04)

        for node in self.datastorage.context['positions']:
            for name, coords in node.items():
                dc.DrawCircle(coords[0]*(width/(2*maxwidth)) + width/2, coords[1]*(height/maxdepth)*0.9 + height*0.04, 8)
                dc.DrawText(name, coords[0]*(width/(2*maxwidth)) + width/2 + 10, coords[1]*(height/maxdepth)*0.9 + height*0.04 - 7)
        dc.Destroy()
