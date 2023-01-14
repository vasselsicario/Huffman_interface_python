from __future__ import annotations
from typing_extensions import Self



class Huffman:
# class HuffmanTree
    class HuffmanTree:
        def __init__(self:Self,char : str | None,freq : int,left : Huffman.HuffmanTree|None=None, right : Huffman.HuffmanTree|None=None):
            """
            constructor of HuffmanTree Node

            @Args:
            char (str|None) : character
            freq (int) : frequence of character 'char'
            left (HuffmanTree) : left child
            right (HuffmanTree) : right child
            """
            
            self._frequence = freq
            self._char=char 
            self._enfant_gauche = left
            self._enfnat_droite = right

        def isLeaf(self : Self) -> bool:
            """ renvoie True si le noeud est une feuille"""
            if self._enfant_gauche == None and self._enfnat_droite == None:
                return True
            
        def __repr__(self):
            _enfant_gauche  : str = ""
            enfant_droit : str = ""
            (_enfant_gauche := 'None') if self._enfant_gauche == None else (_enfant_gauche := str(self._enfant_gauche))
            (enfant_droit := 'None') if self._enfnat_droite == None else (enfant_droit := str(self._enfnat_droite))
            return '(char : \'' + self._char + '\', freq : ' + str(self._frequence) + ', nodes : ' + '{ ' + _enfant_gauche + ', ' + enfant_droit + ' })'
            
            

    @staticmethod
    def buidFreqTable(texte : str) -> list[int]:
        """ construit la table de fréquence"""
        table = [0]*255
        caractere = ""
        for x in range(len(texte)):
            caractere = texte[x]
            table[ord(caractere)] += 1
            
        return  table
    

    def insertHuffmanTreeList(tree : Huffman.HuffmanTree,list : list[Huffman.HuffmanTree])->list[Huffman.HuffmanTree]:
        """insère un arbre dans une liste d’arbres triée"""
        
        for i in range(len(list)):
            if list[i]._frequence >= tree._frequence:
                list.insert(i, tree)
                break    
        if tree not in list:
            list.append(tree)
        return list
        
        
    
    @staticmethod
    def buildTreeList(freqTable : list[int]) -> list[Huffman.HuffmanTree]:
        """ construit la liste triée des arbres feuilles """
        
        tree_list : list[Huffman.HuffmanTree] = []
        for i in range(len(freqTable)):
            if freqTable[i]>0:
                Huffman.insertHuffmanTreeList(Huffman.HuffmanTree(chr(i),freqTable[i]),tree_list)
        return tree_list
    
    

    @staticmethod
    def buildHuffmanTree(freqTable : list[int]) -> HuffmanTree :
        
        #construit un arbre feuille pour chaque caractère présent
        list_feuille_triee : list[Huffman.HuffmanTree]=Huffman.buildTreeList(freqTable)
        #tant que la liste des feuilles n'est pas vide
        while len(list_feuille_triee) > 1 :
            
            #on stock et supprime les 2 premières feuilles de la liste
            x=list_feuille_triee[0]
            y=list_feuille_triee[1]
            list_feuille_triee.pop(0)
            list_feuille_triee.pop(0)
            
            #on creer une branche des 2 feuilles, puis on le rajoute à la liste des "feuilles"
            variable = Huffman.HuffmanTree('',x._frequence+y._frequence,x,y)
            list_feuille_triee.append(variable)
            
            # on retrie par frequences les branches et feuilles
            list_feuille_triee.sort(key=lambda elem: elem._frequence)
            
        return list_feuille_triee
        
        
    
        
    @staticmethod
    def getCodingTable(tree : HuffmanTree,path : chr='',dict={}) -> dict[str,str]:
        """ renvoie le dictionnaire donnant le codage des caractères"""
        if tree._char != '' : 
            dict[tree._char]= path 
        if tree._enfant_gauche != None:
            Huffman.getCodingTable(tree._enfant_gauche, path+'0',dict)

        if tree._enfnat_droite != None:
            Huffman.getCodingTable(tree._enfnat_droite, path+'1',dict)
        return dict
        
    
    
    
    @staticmethod
    def encodeHuffman(texte : str) -> str:
        """ code un texte et renvoie le texte codé et la table de  fréquence"""
        arbre=Huffman.buildHuffmanTree(Huffman.buidFreqTable(texte))
        dict = Huffman.getCodingTable(arbre[0])
        
        text=''
        for i in texte :
            text=text + dict[i]
        return text
    
    def inverser(code:dict):
        """permet d'inverser un dictionnaire pour le codage"""
        d = {}
        for a in code:
            d[code[a]] = a
        return d
    
    def est_prefixe(chiffre1, chiffre2):
        """permet de savoir si 2 chiffres bianires sont préfixes ou pas, pour le decodage"""
        n = len(chiffre1)
        if n<= len(chiffre2) and chiffre2[:n] == chiffre1:
            return True
        else:
            return False
        
    @staticmethod
    def decodeHuffman(texte_binaire, freqs,dbg=False, pad=0):
        """ décode un texte en fonction de la table de fréquence"""

        if texte_binaire == '': return ['']
        
        else:
            cs = [c for c in freqs if Huffman.est_prefixe(c, texte_binaire)]
            resultat = []
            for c in cs:
                m = len(c)
                resultat1 = Huffman.decodeHuffman(texte_binaire[m:], freqs, dbg, pad + 4)
                resultat = resultat + [freqs[c] + s1 for s1 in resultat1]
        return resultat
        
    

    
if __name__ == "__main__" :
    
    texte : str ="Bonjour"
    
    #construction de l'arbre huffman
    treeList = Huffman.buildTreeList(Huffman.buidFreqTable(texte))
    arbre=Huffman.buildHuffmanTree(Huffman.buidFreqTable(texte))
    
    print("table des frequences --> ",Huffman.buidFreqTable(texte))
    print("\n")
    print("dico des codes caractères --> " , Huffman.getCodingTable(arbre[0]))
    print("\n")
    print("arbre de Huffman --> ",str(Huffman.buildTreeList(Huffman.buidFreqTable(texte))))
    print("\n")
    
    #code binaire du texte
    code_binaire=(Huffman.encodeHuffman(texte))
    
    #on inverse le dictionnaire pour coder le code
    dico_inv=Huffman.inverser(Huffman.getCodingTable(arbre[0]))
    
    print(texte," : code codé --> ",Huffman.encodeHuffman(texte))
    print("\n")

    print(Huffman.encodeHuffman(texte),"code décodé -->",Huffman.decodeHuffman(str(Huffman.encodeHuffman(texte)),dico_inv))

    