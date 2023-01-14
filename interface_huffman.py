from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout,QLabel,QHBoxLayout
)
from PyQt6.QtCore import Qt
import sys

from Huffman import Huffman



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        layout2 = QHBoxLayout()
        layout.addLayout(layout2)
        
        self.texte_label :QLabel = QLabel("Texte")
        layout.addWidget(self.texte_label)
        layout2.addWidget(self.texte_label)
        
        self.qline_edit_texte = QLineEdit()
        layout.addWidget(self.qline_edit_texte)
        layout2.addWidget(self.qline_edit_texte)
        
        _qpushButton_entrer = QPushButton("coder / décoder")
        
        layout.addWidget(_qpushButton_entrer)
        
        self.texte_code_label :QLabel = QLabel("Résultat du codage / décodage : ")
        layout.addWidget(self.texte_code_label)
        
        self._resultat:str =''
        self.qline_edit_texte_code = QLabel(self._resultat)
        layout.addWidget(self.qline_edit_texte_code)
        
        self.dico_cc_label :QLabel = QLabel("dictionnaire codage / décodage : ")
        layout.addWidget(self.dico_cc_label)
        
        
        self.qline_dico_cc_code = QLabel()
        layout.addWidget(self.qline_dico_cc_code)
        
        self.arbre_label :QLabel = QLabel("arbre : ")
        self.arbre_label_affichage :QLabel = QLabel()
        layout.addWidget(self.arbre_label)
        layout.addWidget(self.arbre_label_affichage)
        
        
    
        self._entre_svg_decodage:str=''
        
        _qpushButton_entrer.clicked.connect(self.get)
        
    def get(self):
        
        self._dico_code_cc=''
        entree_utilisateur=""
        entree_utilisateur =str(self.qline_edit_texte.text())
        
        
        # si l'entree est un une chaine de caractée our de nombre pour codage ou décodage
        #si décodage
        if(entree_utilisateur.isdigit()):
            
            # on stock l'ancien dico de codage pour décodage
            text2=self._entre_svg_decodage
            self._resultat=''
            
            
            # constructuion de l'arbre de Huffman
        
            arbre=Huffman.buildHuffmanTree(Huffman.buidFreqTable(text2))
            dico = Huffman.getCodingTable(arbre[0])
            
            
            
            print("vous avez choisie de décoder")
            
            #construction du dictionnaire inversé pour décoder
            dico_inv=Huffman.inverser(dico)
            
                
            #on affiche le dictionnaire inverse
            self._arbre_str=dico_inv
            self.qline_dico_cc_code.setText(str(dico_inv))
            
                
            self._resultat=str(Huffman.decodeHuffman(entree_utilisateur,dico_inv))
                
            #on verifie si le décoage est possible avec le bon nombre binaire
            if str(self._resultat)==str([]):
                self.qline_edit_texte_code.setText(" veuiller rajouter un nombre binaire en plus")
            else:
                #on affiche le resultat dans le label
                self.qline_edit_texte_code.setText(str(self._resultat))
            
        
            
        #si codage 
        else:
            # on stock l'ancien dico de codage pour décodage
            self._entre_svg_decodage=entree_utilisateur
            
            # construction de l'arbre Huffman
            arbre = Huffman.buildHuffmanTree(Huffman.buidFreqTable(entree_utilisateur))
            dico = Huffman.getCodingTable(arbre[0])
            
            
            print("vous avez choisie de coder")
            
            #on affiche le resultat dans le label
            self.qline_edit_texte_code.setText(str(Huffman.encodeHuffman(entree_utilisateur)))
                
                
            # afficher le dictionnaire des caractères avec leurs codes
            self.qline_dico_cc_code.setText(str(Huffman.getCodingTable(arbre[0])))
            
            #afficher l'abre de huffman
                
            self.arbre_label_affichage.setText(str(Huffman.buildTreeList(Huffman.buidFreqTable(entree_utilisateur))))
            

if __name__ == "__main__":

    """with open('skills.json', 'r', encoding = 'utf-8') as f:
        dico : list[dict] = json.load(f)"""

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())