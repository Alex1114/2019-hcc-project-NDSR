#ifndef _ROS_SERVICE_SetFSMState_h
#define _ROS_SERVICE_SetFSMState_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace duckietown_msgs
{

static const char SETFSMSTATE[] = "duckietown_msgs/SetFSMState";

  class SetFSMStateRequest : public ros::Msg
  {
    public:
      typedef const char* _state_type;
      _state_type state;

    SetFSMStateRequest():
      state("")
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      uint32_t length_state = strlen(this->state);
      varToArr(outbuffer + offset, length_state);
      offset += 4;
      memcpy(outbuffer + offset, this->state, length_state);
      offset += length_state;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint32_t length_state;
      arrToVar(length_state, (inbuffer + offset));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_state; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_state-1]=0;
      this->state = (char *)(inbuffer + offset-1);
      offset += length_state;
     return offset;
    }

    const char * getType(){ return SETFSMSTATE; };
    const char * getMD5(){ return "af6d3a99f0fbeb66d3248fa4b3e675fb"; };

  };

  class SetFSMStateResponse : public ros::Msg
  {
    public:

    SetFSMStateResponse()
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
     return offset;
    }

    const char * getType(){ return SETFSMSTATE; };
    const char * getMD5(){ return "d41d8cd98f00b204e9800998ecf8427e"; };

  };

  class SetFSMState {
    public:
    typedef SetFSMStateRequest Request;
    typedef SetFSMStateResponse Response;
  };

}
#endif
