#!/usr/bin/python3

"""
  limit the rate at which messages are posted.
  
  'post_rate_limit' is an integer value, the maxium number of messages per second to be permitted
   defaults to 1 message per second.

   usage:

   post_rate_limit 2
   on_post post_rate_limit


"""

import time

from sarra.sr_util import nowflt


class Post_Rate_Limit(object):

    def __init__(self,parent):

        if hasattr(parent,'post_rate_limit'):
            if type(parent.post_rate_limit) is list:
               parent.post_rate_limit = int(parent.post_rate_limit[0])
        else:
            parent.post_rate_limit = 1

        parent.post_rate_limit_msgcount=0
        parent.post_rate_limit_since=nowflt()

        parent.logger.info( "post_rate_limit set to %d messages/second" % parent.post_rate_limit )
          
    def perform(self,parent):

        import time

        now=nowflt()
        time_elapsed=now-parent.post_rate_limit_since

        parent.post_rate_limit_msgcount += 1
        if ( parent.post_rate_limit_msgcount > parent.post_rate_limit ):
            parent.logger.info( "post_rate_limit %d messages/second, sleeping" % parent.post_rate_limit )
            if time_elapsed < 1: 
                time.sleep(1-time_elapsed)
                time_elapsed=1         

        if time_elapsed >= 1 :
            parent.post_rate_limit_msgcount=0
            parent.post_rate_limit_since=nowflt()

        return True

post_rate_limit = Post_Rate_Limit(self)

self.on_post = post_rate_limit.perform

