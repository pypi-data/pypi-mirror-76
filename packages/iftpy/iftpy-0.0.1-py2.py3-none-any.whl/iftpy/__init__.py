__version__='0.0.1'

import json

def floatquantize(n:float,d:float)->float:
    #将n四舍五入到d的整数倍
    return float(int(n/d+0.5)*d)

class Iftpnote():
    '''
    iftp音符类    
    start:起点，单位：小节，float
    end:终点，单位：小节，float
    notenum:音高，与midi相同，即C4为60，音高越高，数值越大，int
    lyric:歌词，str
    '''
    def __init__(self,
                 start:float,
                 end:float,
                 notenum:int,
                 lyric:str):
        self.start=start
        self.end=end
        self.notenum=notenum
        self.lyric=lyric
    
    def __str__(self):
        return "  note {} {} {} {}".format(self.start,
                                           self.end,
                                           self.notenum,
                                           self.lyric)
    
    def dump(self)->dict:
        return {"ADB0": "", 
                "ADB1": "", 
                "AT": self.start, 
                "C": "", 
                "CHA": "", 
                "CP": 0, 
                "DB0": "", 
                "DB1": "", 
                "NH": self.notenum, 
                "P1": 0.2, 
                "P2": 0.8, 
                "RT": self.end, 
                "SH": 0, 
                "SP": 1, 
                "SV": 0, 
                "V1": self.lyric, 
                "V1P": 0, 
                "V2": "", 
                "V2P": 1, 
                "V3": "", 
                "V3P": 1, 
                "mute": False, 
                "name": self.lyric}
    
class Iftptrack():
    '''
    iftp音轨类
    name:音轨名，str
    tempo:曲速，float
    beats:每小节拍数，int
    mute:静音，bool
    solo:独奏，bool
    note:音符列表
    '''
    def __init__(self,
                 name:str="",
                 tempo:float=120.0,
                 beat:int=4,
                 mute:bool=False,
                 solo:bool=False,
                 note:list=[]):
        self.name=name
        self.tempo=tempo
        self.beat=beat
        self.mute=mute
        self.solo=solo
        self.note=note

    def __str__(self):
        s=" track "+self.name
        for n in self.note:
            s+="\n"+str(n)
        return s
    
    def dump(self)->dict:
        notelist=[n.dump() for n in self.note]
        if(len(self.note))==0:
            tracklen=20
        else:
            tracklen=int(self.note[-1].end)+1
        return {"DB0":"",
                "DB1":"",
                "FS":44100,
                "SEG":"",
                "beat":self.beat,
                "effects":
                    [
                        {"Mix":[1]*21000,
                        "data":
                            [
                                {"data":[0]*21000,
                                "maxValue":10,
                                "minValue":-10,
                                "name":"Gain",
                                "normalValue":0
                                },
                                {"data":[0]*21000,
                                "maxValue":1,
                                "minValue":-1,
                                "name":"Pan",
                                "normalValue":0
                                }
                            ],
                        "name":"Mixer"
                        }
                    ],
                "flatsf":[],
                "mute":self.mute,
                "name":self.name,
                "notef":notelist,
                "solo":False,
                "synthesize_engine_add_information":"",
                "tempo":self.tempo,
                "time":tracklen,
                "wavesf":
                    [
                        {"data":[60]*21000,
                         "maxValue":119.5,
                         "minValue":-0.5,
                         "name":"TON",
                         "normalValue":-7
                        },
                        {"data":[0]*21000,
                         "maxValue":6,
                         "minValue":-6,
                         "name":"PIT",
                         "normalValue":0
                        },
                        {"data":[0]*21000,
                         "maxValue":1,
                         "minValue":0,
                         "name":"XSY",
                         "normalValue":0
                        },
                    ],
                "wavetimeat":0
                }
    
    def quantize(self,d:float):
        '''
        将iftp音轨按照给定的分度值d（单位：小节）量化。
        将所有音符的边界四舍五入到d的整数倍，过短的音符将被删除。
        例如，如果1小节4拍，需要量化到1拍，请使用tr.quantize(1/4)
        '''
        notes=[]
        for n in self.note:
            n.start=floatquantize(n.start,d)
            n.end=floatquantize(n.end,d)
            if((n.end-n.start)>0.1*d):
                notes.append(n)
        self.note=notes
        return self      

    def to_midi_track(self):
        '''
        将iftp音轨对象转换为mido.MidiTrack对象
        '''
        import mido
        barlen=480*self.beat
        track=mido.MidiTrack()
        time=0.0
        for n in self.note:
            track.append(mido.MetaMessage('lyrics',text=n.lyric,time=int((n.start-time)*barlen)))
            track.append(mido.Message('note_on', note=n.notenum,velocity=64,time=0))
            track.append(mido.Message('note_off',note=n.notenum,velocity=64,time=int((n.end-n.start)*barlen)))
            time=n.end
        track.append(mido.MetaMessage('end_of_track'))
        return track

    def to_ust_file(self):
        '''
        将iftp音轨对象转换为utaufile.Ustfile对象
        '''
        from utaufile import Ustfile,Ustnote
        ust=Ustfile()
        barlen=480*self.beat
        time=0.0
        for n in self.note:
            if(n.start>time):
                ust.note.append(Ustnote(length=int((n.start-time)*barlen),
                                   lyric="R",notenum=60))
            ust.note.append(Ustnote(length=int((n.end-n.start)*barlen),
                                    lyric=n.lyric,
                                    notenum=n.notenum))    
            time=n.end
        return ust
            
    def to_music21_stream(self):
        '''
        将iftp音轨对象转换为music21 Stream对象
        '''
        import music21
        st=self.to_ust_file().to_music21_stream()
        #节拍
        ts=music21.meter.TimeSignature()
        ts.numerator=self.beat#每小节拍数
        ts.denominator=4#音符分数
        st.insert(0,ts)
        #曲速
        st.insert(0,music21.tempo.MetronomeMark(number=self.tempo))
        return st

    def to_dv_segment(self):
        '''
        将iftp音轨对象转换为dv区段对象
        '''
        import dvfile
        barlen=480*self.beat
        d=dvfile.Dvsegment(start=4*barlen,length=int(self.note[-1].end+1)*1920,name=self.name)
        for n in self.note:
            d.note.append(dvfile.Dvnote(start=int(n.start*barlen),
                                        length=int((n.end-n.start)*barlen),
                                        hanzi=n.lyric,
                                        pinyin=n.lyric,
                                        notenum=n.notenum))
        return d

    def to_dv_track(self):
        '''
        将iftp音轨对象转换为dv音轨对象
        '''
        import dvfile
        return dvfile.Dvtrack(name=self.name,
                              mute=self.mute,
                              solo=self.solo,
                              segment=[self.to_dv_segment()])

class Iftpfile():
    '''
    iftp文件类
    tempo:曲速，float
    beats:每小节拍数，int
    track:音轨列表
    '''
    def __init__(self,
                 tempo:float=120.0,
                 beat:int=4,
                 track:list=[]):
        self.tempo=tempo
        self.beat=beat
        self.track=track
    
    def __str__(self):
        s="Iftpfile {} {}".format(self.tempo,self.beat)
        for tr in self.track:
            s+="\n"+str(tr)
        return s
    
    def dump(self)->dict:
        tracklist=[tr.dump() for tr in [Iftptrack(tempo=self.tempo,beat=self.beat)]+self.track]
        tracklen=max(tr["time"] for tr in tracklist)
        return {"AEG":"",
           "FS":44100,
           "audio_engine_add_information":"",
           "beat":self.beat,
           "editor":"",
           "name":"",
           "tempo":self.tempo,
           "time":tracklen,
           "tracklist":tracklist}
    
    def save(self,filename:str):
        """
        将Iftpfile对象保存为iftp文件
        filename：文件路径与名称
        """
        import json
        with open(filename,"w") as file:
            json.dump(self.dump(),file)
    
    def quantize(self,d:float):
        '''
        将iftp工程按照给定的分度值d（单位：小节）量化。
        将所有音符的边界四舍五入到d的整数倍，过短的音符将被删除。
        例如，如果1小节4拍，需要量化到1拍，请使用ift.quantize(1/4)
        '''
        for tr in self.track:
            tr.quantize(d)
        return self

    def settempo(self,tempo:float=-1.0):
        """
        设置工程曲速为tempo，并同步到所有音轨
        如果tempo<=0，或不输入tempo，则不修改曲速，只同步
        """
        if(tempo<=0):
            tempo=self.tempo
        else:
            self.tempo=tempo
        for tr in self.track:
            tr.tempo=tempo
        return self

    def setbeat(self,beat:int=-1):
        """
        设置工程节拍数为beat，并同步到所有音轨
        如果beat<=0，或不输入beat，则不修改节拍数，只同步
        """
        if(beat<=0):
            beat=self.beat
        else:
            self.beat=beat
        for tr in self.track:
            tr.beat=beat
        return self

    def to_music21_score(self):
        '''
        将iftp文件对象转换为music21 Score对象
        '''
        import music21
        sc=music21.stream.Score()
        for tr in self.track:
            p=music21.stream.Part(tr.to_music21_stream())
            p.partName=tr.name
            sc.append(p)
        return sc

    def to_dv_file(self):
        '''
        将iftp文件对象转换为dv文件对象
        '''
        import dvfile
        dvtracks=[]
        for tr in self.track:
            dvtracks.append(tr.to_dv_track())
        return dvfile.Dvfile(tempo=[(0,self.tempo)],
                             beats=[(-3,self.beat,4)],
                             track=dvtracks)

    def to_ust_file(self):
        '''
        将iftp文件对象转换为utaufile.Ustfile对象列表
        '''
        ust=[]
        for tr in self.track:
            ust.append(tr.to_ust_file())
        return ust

    def to_midi_file(self):
        '''
        将iftp文件对象转换为mido.MidiFile对象
        '''
        import mido
        mid = mido.MidiFile()
        #控制轨
        ctrltrack=mido.MidiTrack()
        ctrltrack.append(mido.MetaMessage('track_name',name='Control',time=0))
        ctrltrack.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(self.tempo),time=0))
        mid.tracks.append(ctrltrack)
        for tr in self.track:
            mid.tracks.append(tr.to_midi_track())
        return mid

def parsenote(notedict:dict):
    return Iftpnote(start=notedict["AT"],
                    end=notedict["RT"],
                    notenum=notedict["NH"],
                    lyric=notedict["name"])
    
def parsetrack(trackdict:dict):
    note=[]
    for notedict in trackdict["notef"]:
        note.append(parsenote(notedict))
    return Iftptrack(name=trackdict["name"],
                     tempo=trackdict["tempo"],
                     beat=trackdict["beat"],
                     mute=trackdict["mute"],
                     solo=trackdict["solo"],
                     note=note)

def openiftp(filename:str):
    """
    打开iftp文件，返回Iftpfile对象
    filename：文件路径与名称
    """
    with open(filename) as file:
        filedict=json.load(file)
    track=[]
    for trackdict in filedict["tracklist"][1:]:
        track.append(parsetrack(trackdict))
    return Iftpfile(tempo=filedict["tempo"],
                    beat=filedict["beat"],
                    track=track)

def main():
    import dvfile
    openiftp(r"C:\Users\lin\Desktop\3.iftp").to_dv_file().save(r"C:\Users\lin\Desktop\x.dv")
    pass

if(__name__=="__main__"):
    main()
