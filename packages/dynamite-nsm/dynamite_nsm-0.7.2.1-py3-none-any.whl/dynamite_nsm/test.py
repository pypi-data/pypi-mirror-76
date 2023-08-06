from dynamite_nsm import utilities
s = """
● logstash.service
     Loaded: loaded (/etc/systemd/system/logstash.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Fri 2020-08-07 12:27:45 EDT; 3 days ago
   Main PID: 1816427 (code=exited, status=143)

Aug 07 12:27:23 jamin-dev logstash[1816427]: WARNING: Please consider reporting this to the maintainers of com.headius.backport9.modules.Modules
Aug 07 12:27:23 jamin-dev logstash[1816427]: WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
Aug 07 12:27:23 jamin-dev logstash[1816427]: WARNING: All illegal access operations will be denied in a future release
Aug 07 12:27:40 jamin-dev logstash[1816427]: Thread.exclusive is deprecated, use Thread::Mutex
Aug 07 12:27:44 jamin-dev logstash[1816427]: Sending Logstash logs to /var/log/dynamite/logstash/ which is now configured via log4j2.properties
Aug 07 12:27:45 jamin-dev logstash[1816427]: [2020-08-07T12:27:45,076][INFO ][logstash.setting.writabledirectory] Creating directory {:setting=>"path.queue", :path=>"/opt/dynamite/logstash/data/queue"}
Aug 07 12:27:45 jamin-dev logstash[1816427]: [2020-08-07T12:27:45,087][INFO ][logstash.setting.writabledirectory] Creating directory {:setting=>"path.dead_letter_queue", :path=>"/opt/dynamite/logstash/data/dead_letter_queue"}
Aug 07 12:27:45 jamin-dev systemd[1]: Stopping logstash.service...
Aug 07 12:27:45 jamin-dev systemd[1]: logstash.service: Succeeded.
Aug 07 12:27:45 jamin-dev systemd[1]: Stopped logstash.service.
"""

print(utilities.wrap_text(s))