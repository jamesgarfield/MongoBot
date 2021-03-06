import os
import re
import pkgutil

from autonomic import axon, help, Dendrite, public, alias
from settings import SAFESET, NICK, HOST, REGISTERED, CONTROL_KEY
from secrets import *
from util import colorize
from time import sleep


# System is stuff relating to the function of the
# the bot and the server. There's some potentially 
# dangerous shit in here.
class System(Dendrite):

    libs = [name for _, name, _ in pkgutil.iter_modules(['brainmeats'])]

    def __init__(self, cortex):
        super(System, self).__init__(cortex)

    # Help menu. It used to just show every command, but there
    # are so goddamn many at this point, they had to be split
    # into categories.
    @axon
    @help("<show this menu>")
    @alias('help')
    def showhelp(self):

        enabled = self.cx.master.ENABLED
        broken = self.cx.broken

        if not self.values or self.values[0] not in self.libs:
            cats = sorted(self.libs)

            cats = [colorize(lib, 'lightgrey') if lib not in enabled else lib for lib in self.libs]
            cats = [colorize(lib, 'red') if lib in broken else lib for lib in cats]

            cats = ', '.join(cats)
            self.chat('%shelp WHAT where WHAT is one of the following: %s' % (CONTROL_KEY, cats))
            return

        which = self.values[0]
        if which in broken:
            return '%s is currently broken.' % which

        if which not in enabled:
            return '%s is not enabled.' % which

        return self.cx.helpmenu[which]

    @axon
    @help("<show editable settings>")
    def settings(self):
        for name, value in SAFESET:
            if self.values and name not in self.values:
                continue
            sleep(1)
            self.chat(name + " : " + str(value))

    # This should be pretty straightforward. Based on BOT_PASS
    # in secrets; nobody can use the bot until they're 
    # registered. Went with flat file for ease of editing
    # and manipulation.
    @axon
    @public
    @help("PASSWORD <register your nick and host to use the bot>")
    def regme(self):
        if not self.values:
            self.chat("Please enter a password.")
            return
        
        if self.values[0] != BOT_PASS:
            self.chat("Not the password.")
            return

        real = self.cx.lastrealsender
        if real in self.cx.REALUSERS:
            self.chat("Already know you, bro.")
            return
        
        self.cx.REALUSERS.append(real)

        users = open(REGISTERED, 'a')
        users.write(real + "\n")
        users.close()

        self.chat("You in, bro.")

    # Rewite a setting in the settings file. Available settings
    # are defined in SAFESET. Do not put SAFESET in the SAFESET.
    # That's just crazy.
    @axon
    @help("SETTING=VALUE <update a " + NICK + " setting>")
    def update(self, inhouse=False):
        if not inhouse:
            vals = self.values

        if not vals or len(vals) != 2:
            self.chat("Must name SETTING and value, please")
            return

        pull = ' '.join(vals)

        if pull.find("'") != -1 or pull.find("\\") != -1 or pull.find("`") != -1:
            self.chat("No single quotes, backtics, or backslashes, thank you.")
            return

        setting, value = pull.split(' ', 1)

        safe = False
        for safesetting, val in SAFESET:
            if setting == safesetting:
                safe = True
                break

        if not safe:
            self.chat("That's not a safe value to change.")
            return

        rewrite = "sed 's/" + setting + " =.*/" + setting + " = " + value + "/'"
        targeting = ' <settings.py >tmp'
        reset = 'mv tmp settings.py'

        os.system(rewrite + targeting)
        os.system(reset)

        self.chat(NICK + " rewrite brain. Feel smarter.")

    # Reloads the bot. Any changes make to cortex or brainmeats
    # and most settings will be reflected after a reload.
    @axon
    @help("<reload " + NICK + ">")
    def reload(self):
        meats = self.cx.brainmeats
        if 'webserver' in meats:
            meats['webserver'].reloadserver(True)
        self.cx.master.reload()

    # Actually kills the medulla process and waits for the 
    # doctor to restart. Some settings and any changes to 
    # medulla.py won't take effect until a reboot.
    @axon
    @alias('seppuku', 'harakiri')
    @help("<set squirrel on fire and staple it to angel. No, really>")
    def reboot(self):
        self.cx.master.die()

    # A shortcut to the update function to change nick. Also
    # tells the irc server.
    @axon
    @help("NICKNAME <change " + NICK + "'s name>")
    def nick(self):
        if not self.values:
            self.chat("Change name to what?")
            return

        name = self.values[0]
        if not re.search("^\w+$", name):
            self.chat("Invalid name")
            return

        self.cx.sock.send('NICK ' + name + '\n')
        self.cx.sock.send('USER ' + IDENT + ' ' + HOST + ' bla :' + REALNAME + '\n')
        self.cx.sock.send('JOIN ' + CHANNEL + '\n')

        self.update(['NICK', name])
        self.reboot()

    # DANGER ZONE. You merge it, anyone can pull it. If you
    # have a catastrophic failure after this, it's probably
    # because of a conflict with local changes. But will it
    # tell you that's what happened? HELL no.
    @axon
    @help("<update from git repo>")
    def gitpull(self):
        os.system("git pull origin master")
        self.cx.master.reload(True)
        self.chat("I know kung-fu.")

    # Turn libs on.
    @axon
    @help("LIB_1 [LIB_n] <activate libraries>")
    def enable(self):
        if not self.values:
            self.chat("Enable what?")
            return

        if self.values[0] == '*':
            values = self.libs
        else:
            values = self.values

        already = []
        nonextant = []
        enabled = []
        broken = []
        for lib in values:
            if lib in self.cx.master.ENABLED:
                already.append(lib) 
            elif lib not in self.libs:
                nonextant.append(lib)
            elif lib in self.cx.broken:
                broken.append(lib)
            else:
                enabled.append(lib)
                self.cx.master.ENABLED.append(lib)

        messages = []
        if len(already):
            messages.append('%s already enabled.' % ', '.join(already))
            
        if len(nonextant):
            messages.append('%s nonexistent.' % ', '.join(nonextant))
            
        if len(broken):
            messages.append('%s done borked.' % ', '.join(broken))
            
        if len(enabled):
            messages.append('Enabled %s.' % ', '.join(enabled))
            
        self.cx.master.reload(True)

        self.chat(' '.join(messages))

    # Turn libs off. Why all this lib stuff? Helps when developing, so
    # you can just turn stuff off while you tinker and prevent crashes.
    @axon
    @help("LIB_1 [LIB_n] <deactivate libraries>")
    def disable(self):
        if not self.values:
            self.chat("Disable what?")
            return

        if 'system' in self.values:
            self.chat("You can't disable the system, jackass.")
            return

        already = []
        nonextant = []
        disabled = []
        for lib in self.values:
            if lib not in self.libs:
                nonextant.append(lib)
            elif lib not in self.cx.master.ENABLED:
                already.append(lib) 
            else:
                disabled.append(lib)
                self.cx.master.ENABLED.remove(lib)

        messages = []
        if len(already):
            messages.append('%s already disabled.' % ', '.join(already))
            
        if len(nonextant):
            messages.append("%s don't exist." % ', '.join(nonextant))
            
        if len(disabled):
            messages.append("Disabled %s." % ', '.join(disabled))
            
        self.cx.master.reload(True)

        self.chat(' '.join(messages))

    # Show secret stuff.
    @axon
    @help("<print api keys and stuff>")
    def secrets(self):
        # TODO: lot of new secrets, add them, or list them and get specific one from values
        items = {
            'WEATHER_API': WEATHER_API,
            'WORDNIK_API': WORDNIK_API,
            'FML_API': FML_API,
            'WOLFRAM_API': WOLFRAM_API,
            'DELICIOUS_USER ': DELICIOUS_USER,
            'DELICIOUS_PASS ': DELICIOUS_PASS,
        }
        for key, val in items.iteritems():
            self.chat(key + ": " + val)

    
