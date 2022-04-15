
########################################################
import maya.cmds as cmds
import maya.api.OpenMaya as newOM


# 01/03 /2022 # created

#################GUI###########################"
# Renaming " adding prefiex and suffixes
#
#
################################################

class MR_Window(object):
        
    #constructor
    
    def __init__(self):
            
        self.window = "MR_Window"
        self.title = " RENAMING-TOOL "
        self.size = (200, 100)
            
        # close old window is open
        
        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window=True)
            
        #create new window
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        
        cmds.columnLayout(adjustableColumn =True)
        cmds.text(self.title)
        
        cmds.separator(h=20)  # --------------------------------------------------------
        
        cmds.text(' select the items that you want to use ')
        
        cmds.separator(h=20)  # --------------------------------------------------------
   
        self.rename_w = cmds.textFieldGrp(label='rename',adj=1)
        self.rename_butt= cmds.button(label = 'rename', command = self.renaming_word)
        
        cmds.separator(h=20) # --------------------------------------------------------
        
        self.tobereplaced = cmds.textFieldGrp(label='To Be Replaced',adj=1)
        self.replace = cmds.textFieldGrp(label='Replacement',adj=1)
        self.replacebutton = cmds.button(label = 'Replace', command = self.replace_with)
        
        self.Prefix = cmds.textFieldButtonGrp( label='Prefix', text='', buttonLabel='Add', adj=1 , bc =self.add_Prefix)
        self.suffix = cmds.textFieldButtonGrp( label='Suffix', text='', buttonLabel='Add', adj=1, bc = self.add_suffix)
        
        cmds.separator(h=20)  # --------------------------------------------------------
        
         
        
        self.number_of_incrementation = cmds.textScrollList( numberOfRows=3, allowMultiSelection=True,append=['0', '00', '000'],selectItem='0', showIndexedItem=4 )
        
        
        cmds.columnLayout(adjustableColumn =True)
        self.increment_button = cmds.button( label = ' Add increment ', c = self.incrementation)

        cmds.separator(h=30)  # --------------------------------------------------------

        self.delete_incremt = cmds.button( label = ' delete last increment ', c = self.delete_the_last_incrementation)
        cmds.separator(h=30)  # --------------------------------------------------------

        self.delete_first_increment = cmds.button( label = ' delete first increment ', c = self.delete_the_first_incrementation)
        print('Renaming Tool is Running')
        
        cmds.showWindow()    
        
    ##############################################################################################################################################################################
    #
    #         FUNCTIONS SECTION 
    #
    #
    ##############################################################################################################################################################################################
    
    def Sorting(self,lst):

        sorting =[]
        lst.sort(key= len , reverse =True)
        for each in lst :
            sorting.append(each)
        return sorting


    # Renaming MObject #############################################################################""

    def nameToNode(self, name, new_name):
        
        selectionList = newOM.MSelectionList()
        selectionList.add( name ) # add to the selection List

        dagMod = newOM.MDagModifier()
        
        m_obj = selectionList.getDependNode(0)

        mfn_dag = newOM.MObject(m_obj)
        dagMod.renameNode(mfn_dag,new_name)
        dagMod.doIt()
    
    #################################################################################

    def show_select(self,*args):
        
        selection = cmds.ls(sl=True)
     
    #################################################################################
        
    def renaming_word(self,*args):

        
        sel = cmds.ls(sl=True)

        
        br = cmds.textFieldGrp(self.rename_w,q=True,text=True)
        if br == None:
            pass
        else:
            for each in sel:
                # get the dag Object
                try:
                    self.nameToNode(each,br)

                except:
                    sel = cmds.ls(sl=True)

                    for each in reversed(sel) :

                        if each == br:
                            pass
                        else:
                            self.nameToNode(each,br)
            
                  
    ######################################################################################"
          
    def replace_with(self,*args):
        
        sel = cmds.ls(sl=True)
        sorting = self.Sorting(sel)

        a = cmds.textFieldGrp(self.tobereplaced,q=True, text=True)
        b = cmds.textFieldGrp(self.replace,q=True,text=True)
         
    
        for each in sorting:


            new = each.rsplit('|')[-1] 
            cmds.rename(each,new.replace(a,b))


        sel = cmds.ls(sl=True)

        for e in reversed(sel):

            if a in e:
                cmds.rename(e,new.replace(a,b))
            

    #############################################################################################################
    
    def add_suffix(self,*args):
     
        sel = cmds.ls(sl=True)

        sorting = self.Sorting(sel)
        a = cmds.textFieldButtonGrp( self.suffix ,q= True ,text= True)

        for each in sorting :
            try:
                last = each.rsplit('|')[-1]
                self.nameToNode(each,last +'_'+a)

            except:
                sel = cmds.ls(sl=True)

                for each in reversed(sel) :

                    if a in each.rsplit('|')[-1] :
                        pass
                    else:
                        last = each.rsplit('|')[-1]
                        self.nameToNode(each, last +'_'+ a)
            

                
            
    ###############################################################################################################
           
    def add_Prefix(self,*args):
     
        sel = cmds.ls(sl=True)

        sorting = self.Sorting(sel)
        a = cmds.textFieldButtonGrp( self.Prefix ,q= True ,text= True)
        
        for each in sorting:
            try:
                last = each.rsplit('|')[-1]
                self.nameToNode(each , a+'_'+last )

            except:
                sel = cmds.ls(sl=True)

                for each in reversed(sel) :

                    if a in each.rsplit('|')[-1] :
                        pass
                    else:
                        last = each.rsplit('|')[-1]
                        self.nameToNode(each , a+'_'+last)
        
        sel = cmds.ls(sl=True)
        for each in sel:
            if '__' in each:
                cmds.rename(each, each.replace('__','_')) 

    #######################################################################################################################
          
    def incrementation(self, *args):
        
        sel = cmds.ls(sl=True)

        sorted_list = self.Sorting(sel)

        num = cmds.textScrollList( self.number_of_incrementation , q=True , selectItem= True )

        
        a = len(sorted_list)

        for each in sorted_list:
            
            last_item = each.rsplit('|')[-1]


            if num[-1] == '000':
                
                cmds.rename(each, last_item+'_000'+str(a))
                a = a - 1
                
            
            elif num[-1] == '00':

                cmds.rename( each, last_item+'_00'+str(a))
                a = a - 1

            elif num[-1] == '0':
                cmds.rename(each, last_item+'_0'+str(a))
                a = a -1

            else:
                cmds.rename(each, each.replace(last_item, last_item +'_'+str(a)) )
                a = a - 1

        for each in sel:

            b= each.count('|')

            while a <= b:
                
                cmds.rename(each, each.replace('1', str(a)))
                    
                if a == b :
                    break
                a+=1

    
    
    ########################################################################################################################
    
    def delete_the_last_incrementation(self,*args):
        
        # get the selection 

        sel = cmds.ls(sl=True)

        
        sorting = self.Sorting(sel)

        for each in sorting:

            last_item_inpath = each.rsplit('|')[-1]
            new = last_item_inpath.replace('_'+last_item_inpath.rsplit('_')[-1],"")


            cmds.rename( each , last_item_inpath.replace(last_item_inpath, new))
            

    #####################################################################################################################################

    def delete_the_first_incrementation(self,*args):
        
        # get the selection 

        sel = cmds.ls(sl=True)

        
        sorting = self.Sorting(sel)

        for each in sorting:

            last_item_inpath = each.rsplit('|')[-1]
     
            length = len('_'+last_item_inpath.rsplit('_')[0])
            new = last_item_inpath[length:]
            
            cmds.rename( each , last_item_inpath.replace(last_item_inpath, new))
            
            
myWindow = MR_Window()


#TriuyenTang