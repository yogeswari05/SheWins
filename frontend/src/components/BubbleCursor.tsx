import { useEffect, useState } from "react";

interface Bubble {
  id: number;
  x: number;
  y: number;
  size: number;
  duration: number;
}

export function BubbleCursor() {
  const [bubbles, setBubbles] = useState<Bubble[]>([]);
  const [nextId, setNextId] = useState(0);

  useEffect(() => {
    const createBubble = (e: MouseEvent) => {
      const newBubble: Bubble = {
        id: nextId,
        x: e.clientX,
        y: e.clientY,
        size: Math.random() * 20 + 10,
        duration: Math.random() * 1000 + 500
      };

      setBubbles(prev => [...prev, newBubble]);
      setNextId(prev => prev + 1);

      // Remove bubble after animation
      setTimeout(() => {
        setBubbles(prev => prev.filter(b => b.id !== newBubble.id));
      }, newBubble.duration);
    };

    const handleClick = (e: MouseEvent) => {
      // Create multiple bubbles on click
      for (let i = 0; i < 5; i++) {
        setTimeout(() => {
          const offsetX = (Math.random() - 0.5) * 30;
          const offsetY = (Math.random() - 0.5) * 30;
          const clickEvent = new MouseEvent('mousemove', {
            clientX: e.clientX + offsetX,
            clientY: e.clientY + offsetY
          });
          createBubble(clickEvent);
        }, i * 50);
      }
    };

    document.addEventListener('mousemove', createBubble);
    document.addEventListener('click', handleClick);

    return () => {
      document.removeEventListener('mousemove', createBubble);
      document.removeEventListener('click', handleClick);
    };
  }, [nextId]);

  return (
    <div className="pointer-events-none fixed inset-0 z-50 overflow-hidden">
      {bubbles.map(bubble => (
        <div
          key={bubble.id}
          className="absolute animate-float-up"
          style={{
            left: bubble.x - bubble.size / 2,
            top: bubble.y - bubble.size / 2,
            width: bubble.size,
            height: bubble.size,
            animation: `floatUp ${bubble.duration}ms ease-out forwards`
          }}
        >
          <div 
            className="w-full h-full rounded-full bg-gradient-to-r from-rose-400/30 to-violet-400/30 backdrop-blur-sm border border-white/20"
            style={{
              boxShadow: '0 0 10px rgba(244, 63, 94, 0.3), 0 0 20px rgba(139, 92, 246, 0.2)'
            }}
          />
        </div>
      ))}
      
      <style jsx>{`
        @keyframes floatUp {
          0% {
            transform: translateY(0) scale(0);
            opacity: 1;
          }
          50% {
            transform: translateY(-20px) scale(1);
            opacity: 0.8;
          }
          100% {
            transform: translateY(-60px) scale(0.5);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
}
