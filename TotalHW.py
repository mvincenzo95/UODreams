#=============================================#
#                 Total HW                    #
#=============================================#
#                                             #
#       Author: Vincenzo Mucciante            #
#       Release Date: 14/09/2018              #
#       Version: 1.0.0                        #
#                                             #
#=============================================#
#                                             #
#   What you need:                            #
#   1) a bag inside your backpack             #
#   2) a bag inside the bank                  #
#   3) a runebook with runes for bank and hw  #
#   4) a beetle                               #
#   Info:                                     #
#   - don't use a bag with the shape          #
#     of a backpack                           #
#=============================================#

import clr, time
clr.AddReference("System.Collections")
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Diagnostics.Process")

from System.Diagnostics import Process
from datetime import datetime
from System.IO import Directory, Path, File
from System.Collections import *
from System.Drawing import Point, Color, Size, Font, FontStyle
from System.Windows.Forms import (LinkLabel, Application, Button, Timer, Form, ComboBox, 
    BorderStyle, GroupBox, Label, TextBox, ListBox, Panel, RadioButton,
    FlatStyle)
from System.ComponentModel import Container

    
###User settings
TrashDelay = 800
DragDelay = 1000
TimeoutOnWaitAction = 1000
###

#General settings
QuestGiverSerial = 0x00006AC1
ContextQuestToggleID = 5
TrashCan = 0x4013FA9E
BoltID = 0x1BFB
Quests = 0
##

class KeepForm(Form):
    ScriptName = 'TotalHW by Rosikcool'
    var = {'start' : datetime.now(), 'recallBank' : 0, 'restockBolt' : 0, 
    'recallHW' : 0, 'enterHW' : 0, 'goingToNPC' : 0, 'deliver' : 0, 'reloadBeetle' : 0,
    'goBack' : 0, 'checkReward' : 0, 'completedQuest' : 0, 'kitHwFound' : 0, 'kitYewFound' : 0,
    'oldTime' : "0001-01-01 00:00:00", 'actualTime' : "0001-01-01 00:00:00", 'beetleSerial' : 0, 'containerBackpack' : 0, 'containerBank' : 0,
    'runebook' : 0, 'minBonus' : 0, 'exBonus' : 0, 'moveAmount' : 0}
    
    def __init__(self):
        self.BackColor = Color.FromArgb(25,25,25)
        self.ForeColor = Color.FromArgb(231,231,231)
        self.Size = Size(320, 330)
        self.Text = '{0}'.format(self.ScriptName)
        self.CenterToScreen()
        self.TopMost = True
        self.LoadFile()
        
        #InfoLabel
        self.Info = Label()
        self.Info.Size = Size(380,15)
        self.Info.Location = Point(0,0)
        self.Info.Text = "Script settings, if u want to change delays, check the code."
        
        #BeetleLabel
        self.Pet = Label()
        self.Pet.Size = Size(200,15)
        self.Pet.Location = Point(0,20)
        self.Pet.Text = "Beetle serial: {0}".format(self.var['beetleSerial'])
        
        #BeetleText
        self.PetT = Button()
        self.PetT.Text = "Set"
        self.PetT.Size = Size(80,20)
        self.PetT.Location = Point(210,15)
        self.PetT.Click += self.setBeetle
        
        #ContainerBackpack
        self.ContainerB = Label()
        self.ContainerB.Size = Size(200,15)
        self.ContainerB.Location = Point(0,40)
        self.ContainerB.Text = "Container backpack serial: {0}".format(self.var['containerBackpack'])
        
        #ContainerBackpackText
        self.ContainerBT = Button()
        self.ContainerBT.Text = "Set"
        self.ContainerBT.Size = Size(80,20)
        self.ContainerBT.Location = Point(210,35)
        self.ContainerBT.Click += self.setContainerBackpack
        
        #ContainerBank
        self.ContainerBank = Label()
        self.ContainerBank.Size = Size(200,15)
        self.ContainerBank.Location = Point(0,60)
        self.ContainerBank.Text = "Container inside bank serial: {0}".format(self.var['containerBank'])
        
        #ContainerBankT
        self.ContainerBankT = Button()
        self.ContainerBankT.Text = "Set"
        self.ContainerBankT.Size = Size(80,20)
        self.ContainerBankT.Location = Point(210,55)
        self.ContainerBankT.Click += self.setContainerBankT
        
        #Runebook
        self.Runebook = Label()
        self.Runebook.Size = Size(200,15)
        self.Runebook.Location = Point(0,80)
        self.Runebook.Text = "Runebook serial: {0}".format(self.var['runebook'])
        
        #RunebookT
        self.RunebookT = Button()
        self.RunebookT.Text = "Set"
        self.RunebookT.Size = Size(80,20)
        self.RunebookT.Location = Point(210,75)
        self.RunebookT.Click += self.setRunebook
        
        #Hints
        self.Hint = Label()
        self.Hint.Size = Size(300,12)
        self.Hint.Location = Point(20,100)
        self.Hint.Text = "1° rune must be a Bank, 2° HW entrance"
        
        #BonusTalismansN
        self.BonusN = Label()
        self.BonusN.Size = Size(150,15)
        self.BonusN.Location = Point(0,120)
        self.BonusN.Text = "Talisman min normal bonus: "
        
        #BonusTalismansNB
        self.BonusNB = TextBox()
        self.BonusNB.Size = Size(30,15)
        self.BonusNB.Location = Point(160,115)
        self.BonusNB.Text = "{0}".format(self.var['minBonus'])
        
        #BonusTalismanNBB
        self.BonusNBB = Button()
        self.BonusNBB.Text = "Set"
        self.BonusNBB.Size = Size(80,20)
        self.BonusNBB.Location = Point(210,110)
        self.BonusNBB.Click += self.setNormalBonus
        
        #BonusTalismansE
        self.BonusE = Label()
        self.BonusE.Size = Size(150,15)
        self.BonusE.Location = Point(0,140)
        self.BonusE.Text = "Talisman: min exept bonus: "
        
        #BonusTalismansEB
        self.BonusEB = TextBox()
        self.BonusEB.Size = Size(30,15)
        self.BonusEB.Location = Point(160,135)
        self.BonusEB.Text = "{0}".format(self.var['exBonus'])
        
        #BonusTalismanEBB
        self.BonusEBB = Button()
        self.BonusEBB.Text = "Set"
        self.BonusEBB.Size = Size(80,20)
        self.BonusEBB.Location = Point(210,140)
        self.BonusEBB.Click += self.setExecBonus
        
        #TrashDelay
        self.Trash = Label()
        self.Trash.Size = Size(300,15)
        self.Trash.Location = Point(0,160)
        self.Trash.Text = "Trash delay: {0} ms".format(TrashDelay)
        
        #DragDelay
        self.Drag = Label()
        self.Drag.Size = Size(300,15)
        self.Drag.Location = Point(0,180)
        self.Drag.Text = "Drag delay: {0} ms".format(DragDelay)
        
        #Timeout
        self.Timeout = Label()
        self.Timeout.Size = Size(300,15)
        self.Timeout.Location = Point(0,200)
        self.Timeout.Text = "Timeout on wait action delay: {0} ms".format(TimeoutOnWaitAction)
        
        #MoveAmount
        self.MoveAmount = Label()
        self.MoveAmount.Size = Size(155,15)
        self.MoveAmount.Location = Point(0,220)
        self.MoveAmount.Text = "Bolts from beetle to backpack: "
        
        #MoveAmountT
        self.MoveAmountT = TextBox()
        self.MoveAmountT.Size = Size(40,15)
        self.MoveAmountT.Location = Point(160,215)
        self.MoveAmountT.Text = "{0} ".format(int(self.var['moveAmount']))
        
        #MoveAmountB
        self.MoveAmountB = Button()
        self.MoveAmountB.Text = "Set"
        self.MoveAmountB.Size = Size(80,20)
        self.MoveAmountB.Location = Point(210,215)
        self.MoveAmountB.Click += self.setMoveAmount
        
        
        #StartButton
        self.btnStart = Button()
        self.btnStart.Text = 'Start'
        self.btnStart.BackColor = Color.FromArgb(50,50,50)
        self.btnStart.Size = Size(50, 30)
        self.btnStart.Location = Point(120, 260)
        self.btnStart.FlatStyle = FlatStyle.Flat
        self.btnStart.FlatAppearance.BorderSize = 1
        self.btnStart.Click += self.btnStartPressed
        
        #DonateLink
        self.btnDonate = Button()
        self.btnDonate.Text = 'Donate'
        self.btnDonate.BackColor = Color.FromArgb(50,50,50)
        self.btnDonate.Size = Size(50, 30)
        self.btnDonate.Location = Point(0, 260)
        self.btnStart.FlatStyle = FlatStyle.Flat
        self.btnStart.FlatAppearance.BorderSize = 1
        self.btnDonate.Click += self.linkDonatePressed
        
        #ResetButton
        self.btnReset = Button()
        self.btnReset.Text = 'Reset Stats'
        self.btnReset.BackColor = Color.FromArgb(50,50,50)
        self.btnReset.Size = Size(90, 30)
        self.btnReset.Location = Point(180, 260)
        self.btnReset.FlatStyle = FlatStyle.Flat
        self.btnReset.FlatAppearance.BorderSize = 1
        self.btnReset.Click += self.btnResetPressed
        
        self.Controls.Add(self.Info)
        self.Controls.Add(self.Pet)
        self.Controls.Add(self.PetT)
        self.Controls.Add(self.ContainerB)
        self.Controls.Add(self.ContainerBT)
        self.Controls.Add(self.ContainerBank)
        self.Controls.Add(self.ContainerBankT)
        self.Controls.Add(self.Runebook)
        self.Controls.Add(self.RunebookT)
        self.Controls.Add(self.Hint)
        self.Controls.Add(self.BonusN)
        self.Controls.Add(self.BonusE)
        self.Controls.Add(self.BonusNB)
        self.Controls.Add(self.BonusNBB)
        self.Controls.Add(self.BonusEB)
        self.Controls.Add(self.BonusEBB)
        self.Controls.Add(self.Trash)
        self.Controls.Add(self.Drag)
        self.Controls.Add(self.Timeout)
        self.Controls.Add(self.MoveAmount)
        self.Controls.Add(self.MoveAmountT)
        self.Controls.Add(self.MoveAmountB)
        self.Controls.Add(self.btnStart)   
        self.Controls.Add(self.btnReset)
        self.Controls.Add(self.btnDonate)
            
    def btnStartPressed(self, send, args):
        self.var["beetleSerial"] = self.PetT.Text
        self.var["containerBank"] = self.ContainerBT.Text
        self.var["containerBackpack"] = self.ContainerBankT.Text
        self.var["minBonus"] = self.BonusNB.Text
        self.var["exBonus"] = self.BonusEB.Text
        self.var["runebook"] = self.RunebookT.Text
        
        self.Flags()
        
        self.Controls.Remove(self.Info)
        self.Controls.Remove(self.Pet)
        self.Controls.Remove(self.PetT)
        self.Controls.Remove(self.ContainerB)
        self.Controls.Remove(self.ContainerBT)
        self.Controls.Remove(self.ContainerBank)
        self.Controls.Remove(self.ContainerBankT)
        self.Controls.Remove(self.Runebook)
        self.Controls.Remove(self.RunebookT)
        self.Controls.Remove(self.Hint)
        self.Controls.Remove(self.BonusN)
        self.Controls.Remove(self.BonusE)
        self.Controls.Remove(self.BonusNB)
        self.Controls.Remove(self.BonusNBB)
        self.Controls.Remove(self.BonusEB)
        self.Controls.Remove(self.BonusEBB)
        self.Controls.Remove(self.Trash)
        self.Controls.Remove(self.Drag)
        self.Controls.Remove(self.Timeout)
        self.Controls.Remove(self.MoveAmount)
        self.Controls.Remove(self.MoveAmountT)
        self.Controls.Remove(self.MoveAmountB)
        self.Controls.Remove(self.btnStart)
        self.Controls.Remove(self.btnReset)
        self.Controls.Remove(self.btnDonate)
        
        self.LoadFile()
        self.var["oldTime"] = datetime.strptime(str(self.var["oldTime"]),"%Y-%m-%d %H:%M:%S")
        
        #TimePassed
        self.TimePassed = Label()
        self.TimePassed.Size = Size(380,15)
        self.TimePassed.Location = Point(0,15)
        self.var["actualTime"] = datetime.now() - self.var["start"]
        self.TimePassed.Text = "Time " + str((self.var["actualTime"] + self.var["oldTime"]).time())
        
        #Step
        self.Step = Label()
        self.Step.Size = Size(380,15)
        self.Step.Location = Point(0,30)
        self.Step.Text = "Step: ..."
        
        #CompletedQuests
        self.CompletedQuests = Label()
        self.CompletedQuests.Size = Size(380,15)
        self.CompletedQuests.Location = Point(0,45)
        self.CompletedQuests.Text = "Completed quests: {0}".format(self.var["completedQuest"])
        
        #KitYewFound
        self.KitYewFound = Label()
        self.KitYewFound.Size = Size(380,15)
        self.KitYewFound.Location = Point(0,60)
        self.KitYewFound.Text = "Kit yew found: {0}".format(self.var["kitYewFound"])
        
        #KitHwFound
        self.KitHwFound = Label()
        self.KitHwFound.Size = Size(380,15)
        self.KitHwFound.Location = Point(0,75)
        self.KitHwFound.Text = "Kit hw found: {0}".format(self.var["kitHwFound"])
        
        #StopButton
        self.btnStop = Button()
        self.btnStop.Text = 'Stop'
        self.btnStop.BackColor = Color.FromArgb(50,50,50)
        self.btnStop.Size = Size(50, 30)
        self.btnStop.Location = Point(30, 260)
        self.btnStop.FlatStyle = FlatStyle.Flat
        self.btnStop.FlatAppearance.BorderSize = 1
        self.btnStop.Click += self.btnStopPressed
        
        #PauseButton
        self.btnPause = Button()
        self.btnPause.Text = 'Pause'
        self.btnPause.BackColor = Color.FromArgb(50,50,50)
        self.btnPause.Size = Size(50, 30)
        self.btnPause.Location = Point(230, 260)
        self.btnPause.FlatStyle = FlatStyle.Flat
        self.btnPause.FlatAppearance.BorderSize = 1
        self.btnPause.Click += self.btnPausePressed
        
        self.Controls.Add(self.Step)
        self.Controls.Add(self.CompletedQuests)
        self.Controls.Add(self.KitYewFound)
        self.Controls.Add(self.KitHwFound)
        self.Controls.Add(self.btnPause)
        self.Controls.Add(self.btnStop)
        #self.Controls.Add(self.TimePassed)
        
        #Timer
        self.time = Timer(Container())
        self.time.Enabled = True
        self.time.Interval = 20
        self.time.Tick += self.OnTick
        
        #Timer2
        self.time2 = Timer(Container())
        self.time2.Enabled = False
        self.time2.Interval = 999
        self.time2.Tick += self.OnTick2

    def linkDonatePressed(self, send, args):
        Process.Start("IExplore", 'paypal.me/vincenzomucciante')
        
    def btnPausePressed(self, send, args):
        self.Step.Text = "Paused."
        self.time.Enabled = False
        self.time2.Enabled = False
        self.Controls.Remove(self.btnPause)
        self.Controls.Remove(self.btnStop)
        
        #ResumeButton
        self.btnResume = Button()
        self.btnResume.Text = 'Resume'
        self.btnResume.BackColor = Color.FromArgb(50,50,50)
        self.btnResume.Size = Size(70, 30)
        self.btnResume.Location = Point(120, 260)
        self.btnResume.FlatStyle = FlatStyle.Flat
        self.btnResume.FlatAppearance.BorderSize = 1
        self.btnResume.Click += self.btnResumePressed
        
        self.Controls.Add(self.btnResume)
        
    def btnResumePressed(self, send, args):
        self.Controls.Remove(self.btnResume)
        self.Controls.Add(self.btnPause)
        self.Controls.Add(self.btnStop)
        self.time.Enabled = True
        self.time2.Enabled = False
        
    def btnStopPressed(self, send, args):
        self.Flags()
        self.Update()
        self.Step.Text = "Finish."
        self.time2.Enabled = False
        self.time.Enabled = False
        self.Update()
        self.Controls.Remove(self.btnStop)
        self.Controls.Remove(self.btnPause)
    
    def btnResetPressed(self, send, args):
        self.var["completedQuest"] = 0
        self.var["actualTime"] = "0001-01-01 00:00:00"
        self.var["oldTime"] = "0001-01-01 00:00:00"
        self.var["kitHwFound"] = 0
        self.var["kitYewFound"] = 0
    
    def setBeetle(self, send, args):
        self.var["beetleSerial"] = hex(Target.PromptTarget())
        self.Update()
        self.Pet.Text = "Beetle serial: {0}".format(self.var['beetleSerial'])
      
    def setContainerBackpack(self, send, args):
        self.var['containerBackpack'] = hex(Target.PromptTarget())
        self.Update()
        self.ContainerB.Text = "Container backpack serial: {0}".format(self.var['containerBackpack'])
    
    def setContainerBankT(self, send, args):
        self.var["containerBank"] = hex(Target.PromptTarget())
        self.Update()
        self.ContainerBank.Text = "Container inside bank serial: {0}".format(self.var['containerBank'])
        
    def setRunebook(self, send, args):
        self.var["runebook"] = hex(Target.PromptTarget())
        self.Update()
        self.Runebook.Text = "Runebook serial: {0}".format(self.var['runebook'])
    
    def setNormalBonus(self, send, args):
        self.var['minBonus'] = int(self.BonusNB.Text)
        self.Update()
        self.BonusNB.Text = "{0}".format(self.var['minBonus'])
        self.BonusNB.ReadOnly = True
    
    def setExecBonus(self, send, args):
        self.var['exBonus'] = int(self.BonusEB.Text)
        self.Update()
        self.BonusEB.Text = "{0}".format(self.var['exBonus'])
        self.BonusEB.ReadOnly = True
    
    def setMoveAmount(self, send, args):
        self.var['moveAmount'] = int(self.MoveAmountT.Text)
        self.Update()
        self.MoveAmountT.Text = "{0} ".format(self.var['moveAmount'])
        self.MoveAmountT.ReadOnly = True
        
    def OnTick2(self, send, args):
        self.var["actualTime"] = datetime.now() - self.var["start"]
        self.TimePassed.Text = "Time " + str((self.var["actualTime"] + self.var["oldTime"]).time())
        
    def OnTick(self, send, args):
        self.CompletedQuests.Text = "Completed quests: {0}".format(str(self.var["completedQuest"]))
        self.KitYewFound.Text = "Kit yew found: {0}".format(str(self.var["kitYewFound"]))
        self.KitHwFound.Text = "Kit hw found: {0}".format(str(self.var["kitHwFound"]))
        if int(self.var["recallBank"]) == 0:
            if not "Checking" in self.Step.Text:
                self.Step.Text = "Checking if need to restock."
            self.Bank()
        elif int(self.var["restockBolt"]) == 0:
            if not "Restocking" in self.Step.Text:
                self.Step.Text = "Restocking bolt."
            self.RestockBolt()
        elif int(self.var["recallHW"]) == 0:
            if not "Going" in self.Step.Text:
                self.Step.Text = "Going back HW."
            self.RecallHW()
        elif int(self.var["enterHW"]) == 0:
            if not "Entering" in self.Step.Text:
                self.Step.Text = "Entering HW."
            self.EnterHW()
        elif int(self.var["goingToNPC"]) == 0:
            if not "Finding" in self.Step.Text:
                self.Step.Text = "Finding NPC."
            self.GoNPC()
        elif int(self.var["deliver"]) == 0:
            if not "Delivering" in self.Step.Text:
                self.Step.Text = "Delivering."
            self.Deliver()
        elif int(self.var["reloadBeetle"]) == 0:
            if not "Realoading" in self.Step.Text:
                self.Step.Text = "Reloading from beetle."
            self.ReloadBeetle()
        elif int(self.var["goBack"]) == 0:
            if not "Going" in self.Step.Text:
                self.Step.Text = "Going back."
            self.GoBack()
        elif int(self.var["checkReward"]) == 0:
            self.CheckReward()
        else:
            Misc.NoOperation()

    def RecallBank(self):
        Items.UseItem(int(self.var['runebook'],16))
        Gumps.WaitForGump(1431013363, 10000)
        Gumps.SendAction(1431013363, 5)
        Misc.Pause(500)
        
    def Bank(self):
        self.var["reloadBeetle"] = 1
        self.var["goBack"] = 1
        if Items.ContainerCount(Player.Backpack, BoltID, 0) > 9:
            self.var["recallBank"] = 1
            self.var["restockBolt"] = 1
        else:
            fil = Mobiles.Filter()
            fil.Enabled = True
            fil.RangeMax = 12
            found = 0
            vendors = Mobiles.ApplyFilter(fil)
            if len(vendors) > 0:
                for vendor in vendors:
                    if "banker" in vendor.Name:
                        found = found +1
                if found == 0:
                    self.RecallBank()
                else:
                    self.var["recallBank"] = 1
                    self.var["restockBolt"] = 0
                    self.var["goBack"] = 1
            else:
                self.RecallBank()
        
    def RestockBolt(self):
        Misc.Pause(150)
        Player.ChatSay(52, "bank")
        while not Items.FindBySerial(int(self.var['containerBank'],16)):
            Misc.Pause(50)
        Items.UseItem(int(self.var['containerBank'],16))
        Misc.Pause(150)
        Mobiles.UseMobile(Player.Serial)
        while Player.Mount:
            Misc.Pause(100)
        beetle = Mobiles.FindBySerial(int(self.var['beetleSerial'],16))
        Items.WaitForContents(beetle.Backpack, TimeoutOnWaitAction)
        if Items.ContainerCount(beetle.Backpack, BoltID, 0) < 10:
            if Items.ContainerCount(Items.FindBySerial(int(self.var['containerBank'],16)), BoltID, 0) > 0:
                for numbolt in Items.FindBySerial(int(self.var['containerBank'],16)).Contains:
                    if numbolt.ItemID == BoltID:
                        Items.Move(numbolt, beetle.Backpack, 16000)
                        break
                Misc.Pause(DragDelay)
                for numbolt in Items.FindBySerial(int(self.var['containerBank'],16)).Contains:
                    if numbolt.ItemID == BoltID:       
                        Items.Move(numbolt, Player.Backpack, 4000)
                        break
                Misc.Pause(DragDelay)
            else:
                self.Step.Text = "No more bolts."
                self.Step.Font = Font("Arial", 10, FontStyle.Bold);
                self.time.Enabled = False
                self.Controls.Remove(self.btnStop)
                self.Controls.Remove(self.btnPause)
        Mobiles.UseMobile(beetle)
        for items in Items.FindBySerial(int(self.var['containerBackpack'],16)).Contains:
            if items.ItemID == 0x1022 and (items.Hue == 0x04A9 or items.Hue == 0x04A8) :
                Items.Move(items, Items.FindBySerial(int(self.var['containerBank'],16)), 0)
                Misc.Pause(DragDelay)
        self.var["restockBolt"] = 1
        self.var["recallHW"] = 0
        
    def RecallHW(self):
        if not Items.FindBySerial(0x403203A5):
            Items.UseItem(int(self.var['runebook'],16))
            Gumps.WaitForGump(1431013363, 10000)
            Gumps.SendAction(1431013363, 11)
            Misc.Pause(500)
        else:
            self.var["recallHW"] = 1
            self.var["enterHW"] = 0
    
    def EnterHW(self):
        if not Items.FindBySerial(0x403240AC):
            Gate = Items.FindBySerial(0x403203A5)
            Player.PathFindTo(Gate.Position.X,Gate.Position.Y,Gate.Position.Z)
        else:
            self.var["enterHW"] = 1
            self.var["goingToNPC"] = 0
    
    def GoNPC(self):
        if not Mobiles.FindBySerial(QuestGiverSerial):
            while Player.Position.X != 6986 or Player.Position.Y != 339:
                Player.PathFindTo(535,992,0)
                Misc.Pause(200)
            while Player.Position.X != 6994 or Player.Position.Y != 349:
                Player.PathFindTo(6994,349,0)
                Misc.Pause(200)
            while Player.Position.X != 7005 or Player.Position.Y != 361:
                Player.PathFindTo(7005,361,0)
                Misc.Pause(200)
            while Player.Position.X != 7015 or Player.Position.Y != 370:    
                Player.PathFindTo(7015,370,0)
                Misc.Pause(200)
            while Player.Position.X != 7024 or Player.Position.Y != 378:    
                Player.PathFindTo(7024,378,0)
                Misc.Pause(200)
            while Player.Position.X != 7037 or Player.Position.Y != 378:        
                Player.PathFindTo(7037,378,0)
                Misc.Pause(200)
            Misc.Pause(50)
            Items.UseItem(int(self.var['containerBackpack'],16))
            Misc.Pause(50)
        else:
            self.var["goingToNPC"] = 1
            self.var["deliver"] = 0
   
    def Deliver(self):
        if Items.BackpackCount(BoltID, 0) < 10:      
            self.var["deliver"] = 1
            self.var["reloadBeetle"] = 0
        else:
            Gumps.ResetGump()
            Mobiles.UseMobile(QuestGiverSerial)
            Gumps.WaitForGump(2770237747, TimeoutOnWaitAction)
            if Gumps.LastGumpGetLine(1) == "Lethal Darts":
                quests = int(self.var["completedQuest"]) +1
                self.var["completedQuest"] = quests
                Gumps.WaitForGump(2770237747, TimeoutOnWaitAction)
                Gumps.SendAction(2770237747, 1)  
                Misc.WaitForContext(Player.Serial, TimeoutOnWaitAction)
                Misc.ContextReply(Player.Serial, ContextQuestToggleID)
                Target.WaitForTarget(TimeoutOnWaitAction)
                for itemcontenuti in Player.Backpack.Contains:
                    if itemcontenuti.ItemID == BoltID:
                        bolt = itemcontenuti.Serial
                Target.TargetExecute(bolt)  
                Target.WaitForTarget(TimeoutOnWaitAction)
                Target.Cancel()
                Mobiles.UseMobile(QuestGiverSerial)
                Gumps.WaitForGump(323772612, TimeoutOnWaitAction)
                Gumps.SendAction(323772612, 1)
                self.var["deliver"] = 1
                self.var["checkReward"] = 0
                
    def CheckReward(self):
        self.var["checkReward"] = 1
        for backpackItems in Player.Backpack.Contains:
            if backpackItems.ItemID == 0x0E75:
                Items.WaitForContents(backpackItems, TimeoutOnWaitAction)
                for rewcontain in backpackItems.Contains:
                    if rewcontain.ItemID == 0x1022 and (rewcontain.Hue == 0x04A9 or rewcontain.Hue == 0x04A8) :
                        Items.Move(rewcontain, Items.FindBySerial(int(self.var["containerBackpack"],16)), 0)
                        if rewcontain.Hue == 0x4A8:
                            self.var["kitYewFound"] = int(self.var["kitYewFound"]) +1
                        else:
                            self.var["kitHwFound"] = int(self.var["kitHwFound"]) +1
                        Misc.Pause(DragDelay)
                    #elif rewcontain.ItemID == 0x108A or rewcontain.ItemID == 0x1F09 or rewcontain.ItemID == 0x1F06 or rewcontain.ItemID == 0x1086:
                        #self.CheckJewels(rewcontain)  
                    elif "Talisman" in rewcontain.Name:
                        self.CheckTalisman(rewcontain)
                Items.Move(backpackItems, Items.FindBySerial(TrashCan), 0) 
                Misc.Pause(TrashDelay)
        self.var["deliver"] = 0
         
    def CheckJewels(self,jewel):
        ContainerBackpack = int(self.var['containerBackpack'],16)
        Items.WaitForProps(jewel, TimeoutOnWaitAction)
        if len(Items.GetPropStringList(jewel)) >= 6:
            if Items.GetPropValue(jewel.Serial, "Faster Cast Recovery") >= 2:
                Items.Move(jewel, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)
            elif Items.GetPropValue(jewel.Serial, "Enhance Potions") >= 15:
                Items.Move(jewel, Items.FindBySerial(ContainerBackpack), 0)
                Misc.Pause(DragDelay)
        
    def CheckTalisman(self, tal):
        ContainerBackpack = int(self.var['containerBackpack'],16)
        Items.WaitForProps(tal, TimeoutOnWaitAction)
        MinNormalBonus = int(self.var['minBonus'])
        MinExBonus = int(self.var['exBonus'])
        if Items.GetPropValue(tal.Serial, "Tinkering Exceptional Bonus") >= MinExBonus and Items.GetPropValue(tal.Serial, "Tinkering Bonus") >= MinNormalBonus:
            Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
            Misc.Pause(DragDelay)   
        elif Items.GetPropValue(tal.Serial, "Fletching Exceptional Bonus") >= MinExBonus and Items.GetPropValue(tal.Serial, "Fletching Bonus") >= MinNormalBonus:
            Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
            Misc.Pause(DragDelay)           
        elif Items.GetPropValue(tal.Serial, "Tailoring Exceptional Bonus") >= MinExBonus and Items.GetPropValue(tal.Serial, "Tailoring Bonus") >= MinNormalBonus:
            Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
            Misc.Pause(DragDelay)       
        elif Items.GetPropValue(tal.Serial, "Blacksmithing Exceptional Bonus") >= MinExBonus and Items.GetPropValue(tal.Serial, "Blacksmithing Bonus") >= MinNormalBonus:
            Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
            Misc.Pause(DragDelay)           
        elif Items.GetPropValue(tal.Serial, "Inscription Exceptional Bonus") >= MinExBonus and Items.GetPropValue(tal.Serial, "Inscription Bonus") >= MinNormalBonus:
            Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
            Misc.Pause(DragDelay)      
        elif Items.GetPropValue(tal.Serial, "Cooking Exceptional Bonus") >= MinExBonus and Items.GetPropValue(tal.Serial, "Cooking Bonus") >= MinNormalBonus:
            Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
            Misc.Pause(DragDelay)         
        elif Items.GetPropValue(tal.Serial, "Alchemy Exceptional Bonus") >= MinExBonus and Items.GetPropValue(tal.Serial, "Alchemy Bonus") >= MinNormalBonus:
            Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
            Misc.Pause(DragDelay)       
        elif Items.GetPropValue(tal.Serial, "Carpentry Exceptional Bonus") >= MinExBonus and Items.GetPropValue(tal.Serial, "Carpentry Bonus") >= MinNormalBonus:
            Items.Move(tal, Items.FindBySerial(ContainerBackpack), 0)
            Misc.Pause(DragDelay)          
        
    def ReloadBeetle(self):
        Mobiles.UseMobile(Player.Serial)
        while Player.Mount:
            Misc.Pause(100)
        beetle = Mobiles.FindBySerial(int(self.var['beetleSerial'],16))
        Items.WaitForContents(beetle.Backpack, TimeoutOnWaitAction)
        if Items.ContainerCount(beetle.Backpack, BoltID, 0) > 10:
            if Items.ContainerCount(Player.Backpack, BoltID, 0) < 10:
                for itemcontenuti in beetle.Backpack.Contains:
                    found = 0
                    if itemcontenuti.ItemID == BoltID and found == 0:       
                        Items.Move(itemcontenuti, Player.Backpack, int(self.var['moveAmount'])) 
                        Misc.Pause(DragDelay)
                        found = 1
            else:
                Mobiles.UseMobile(beetle)
                while not Player.Mount:
                    Misc.Pause(100)
                self.var["reloadBeetle"] = 1
                self.var["deliver"] = 0
        else:
            Mobiles.UseMobile(beetle)
            while not Player.Mount:
                Misc.Pause(100)
            self.var["reloadBeetle"] = 1
            if Items.ContainerCount(Player.Backpack, BoltID, 0) < 10:
                self.var["goBack"] = 0
            else:
                self.var["deliver"] = 0
            
    def GoBack(self):
        if not Items.FindBySerial(0x403203A5):
            while Player.Position.X != 7021 and Player.Position.Y != 372:
                Player.PathFindTo(7021,372,0)
                Misc.Pause(200)
            while Player.Position.X != 7005 and Player.Position.Y != 361:    
                Player.PathFindTo(7005,361,0)
                Misc.Pause(200)
            while Player.Position.X != 6994 and Player.Position.Y != 349:      
                Player.PathFindTo(6994,349,0)
                Misc.Pause(200)
            while Player.Position.X != 538 and Player.Position.Y != 992:   
                Player.PathFindTo(6984,338,0)
                Misc.Pause(200)    
        else:
            self.var["goBack"] = 1
            self.var["recallBank"] = 0
           
    def LoadFile(self):
        f = ""
        if not File.Exists("HW.txt"):
            f = open("HW.txt","w+")
            for item in self.var:
                f.write(item + "=" + str(self.var.get(item))+"\n")
            f.close()
        with open("HW.txt") as myfile:
            for line in myfile:
                name,value = line.partition("=")[::2]
                if not "start" in name.strip():
                    self.var[name.strip()] = value.rstrip()
     
    def Update(self):
        file = open("HW.txt","w")
        file.seek(0,0)
        for item in self.var:
            file.write(item + "=" + str(self.var.get(item))+"\n")
        file.close()
            
    def Flags(self):
        self.var["recallBank"] = 0
        self.var["restockBolt"] = 0
        self.var["recallHW"] = 0
        self.var["enterHW"] = 0
        self.var["deliver"] = 0
        self.var["reloadBeetle"] = 0
        self.var["goingToNPC"] = 0
        self.var["goBack"] = 0
        self.var["checkReward"] = 0
              
form = KeepForm()
Application.Run(form)
        