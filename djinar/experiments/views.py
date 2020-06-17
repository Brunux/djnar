import asyncio
import json
import platform
import logging
import os
import uuid

from django.conf import settings
from django.views.generic import TemplateView, View
from django.http.response import HttpResponse
from django.utils.decorators import classonlymethod
from braces.views import CsrfExemptMixin

from av import VideoFrame
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder

from djinar.experiments.video import VideoTransformTrack


logger = logging.getLogger("pc")
pcs = set()


class WebcamView(TemplateView):
    """
    """
    template_name = 'experiments/webcam.html'


class WebcamOfferView(CsrfExemptMixin, View):
    """
    """
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def post(self, request, *args, **kwargs):
        """
        """
        params = json.loads(request.body)
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        pcs.add(pc)

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("ICE connection state is %s" % pc.iceConnectionState)
            if pc.iceConnectionState == "failed":
                await pc.close()
                pcs.discard(pc)

        # # open media source
        # if args.play_from:
        #     player = MediaPlayer(args.play_from)
        # else:
        options = {"framerate": "30", "video_size": "640x480"}
        if platform.system() == "Darwin":
            player = MediaPlayer("default:none", format="avfoundation", options=options)
        else:
            player = MediaPlayer("/dev/video0", format="v4l2", options=options)

        await pc.setRemoteDescription(offer)
        for t in pc.getTransceivers():
            if t.kind == "audio" and player.audio:
                pc.addTrack(player.audio)
            elif t.kind == "video" and player.video:
                pc.addTrack(player.video)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return HttpResponse(
            json.dumps({
                "sdp": pc.localDescription.sdp, "type": pc.localDescription.type
            }),
            content_type="application/json",
        )


class ServerView(TemplateView):
    """
    """
    template_name = 'experiments/server.html'


class ServerOfferView(CsrfExemptMixin, View):
    """
    """
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def post(self, request, *args, **kwargs):
        """
        """
        params = json.loads(request.body)
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        pc_id = "PeerConnection(%s)" % uuid.uuid4()
        pcs.add(pc)

        def log_info(msg, *args):
            logger.info(pc_id + " " + msg, *args)

        log_info("Created for %s", request.get_host())

        # prepare local media
        player = MediaPlayer(os.path.join(
            settings.BASE_DIR, "djinar/experiments/media/Scott_Holmes_-_04_-_Upbeat_Party.mp3")
        )
        # no recorder for now.
        recorder = MediaBlackhole()

        @pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(message):
                if isinstance(message, str) and message.startswith("ping"):
                    channel.send("pong" + message[4:])

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            log_info("ICE connection state is %s", pc.iceConnectionState)
            if pc.iceConnectionState == "failed":
                await pc.close()
                pcs.discard(pc)

        @pc.on("track")
        def on_track(track):
            log_info("Track %s received", track.kind)

            if track.kind == "audio":
                pc.addTrack(player.audio)
                recorder.addTrack(track)
            elif track.kind == "video":
                local_video = VideoTransformTrack(
                    track, transform=params["video_transform"]
                )
                pc.addTrack(local_video)

            @track.on("ended")
            async def on_ended():
                log_info("Track %s ended", track.kind)
                await recorder.stop()

        # handle offer
        await pc.setRemoteDescription(offer)
        await recorder.start()

        # send answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return HttpResponse(
            json.dumps({
                "sdp": pc.localDescription.sdp, "type": pc.localDescription.type
            }),
            content_type="application/json",
        )
