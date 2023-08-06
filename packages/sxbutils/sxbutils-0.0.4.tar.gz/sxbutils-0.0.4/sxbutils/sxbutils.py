import os

def do_stuff():
    print ("Manchester United")

def validate_envvars(envvars):

    m="validate_envvars"

    count=0
    try:
       for envvar in envvars:
          count += 1
          print(m+" "+envvar.name)
          if not envvar.name in os.environ and envvar.required:
              message=m+" missing envvar ("+envvar.name+") and it is required"
              raise Exception(message)

    except Exception as e:
       message=m+" An exception occurred, error="+str(e)+""
       raise Exception(message)

    finally:
       print(m+" Finally")

