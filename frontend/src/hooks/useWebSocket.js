import { useEffect, useRef, useState } from 'react'
import { getSession } from '../lib/api'

const WS_URL =
  import.meta.env.VITE_WS_URL || 'ws://127.0.0.1:8000/ws/health'

export default function useWebSocket(enabled = true) {
  const [connected, setConnected] = useState(false)
  const [latestReading, setLatestReading] = useState(null)
  const [latestAlert, setLatestAlert] = useState(null)
  const socketRef = useRef(null)

  useEffect(() => {
    if (!enabled) return

    let socket
    let reconnectTimer
    let manuallyClosed = false

    function connect() {
      const session = getSession()

      if (!session?.access_token) return

      socket = new WebSocket(WS_URL)
      socketRef.current = socket

      socket.onopen = () => {
        socket.send(
          JSON.stringify({
            type: 'authenticate',
            access_token: session.access_token,
          })
        )
      }

      socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)

          if (message.type === 'connected') {
            setConnected(true)
          }

          if (message.type === 'health_update') {
            setLatestReading(message.data)
            window.dispatchEvent(
              new CustomEvent('astrohealth:health-update', {
                detail: message.data,
              })
            )
          }

          if (message.type === 'new_alert') {
            setLatestAlert(message.data)
            window.dispatchEvent(
              new CustomEvent('astrohealth:new-alert', {
                detail: message.data,
              })
            )
          }

          if (message.type === 'ping') {
            socket.send(JSON.stringify({ type: 'pong' }))
          }
        } catch (error) {
          console.error('WebSocket message error:', error)
        }
      }

      socket.onclose = () => {
        setConnected(false)

        if (!manuallyClosed) {
          reconnectTimer = setTimeout(connect, 3000)
        }
      }

      socket.onerror = () => {
        setConnected(false)
      }
    }

    connect()

    return () => {
      manuallyClosed = true
      clearTimeout(reconnectTimer)

      if (socket && socket.readyState < WebSocket.CLOSING) {
        socket.close()
      }

      setConnected(false)
    }
  }, [enabled])

  return {
    connected,
    latestReading,
    latestAlert,
  }
}