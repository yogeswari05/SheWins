import React from 'react';

interface LoadingSkeletonProps {
  className?: string;
  children?: React.ReactNode;
}

export function LoadingSkeleton({ className = '', children }: LoadingSkeletonProps) {
  return (
    <div className={`animate-pulse ${className}`}>
      <div className="h-full bg-gradient-to-r from-white/10 via-white/20 to-white/10 rounded-lg"></div>
      {children}
    </div>
  );
}

export function CardSkeleton({ className = '' }: LoadingSkeletonProps) {
  return (
    <LoadingSkeleton className={`p-6 ${className}`}>
      <div className="space-y-4">
        <div className="h-4 bg-white/20 rounded w-1/4"></div>
        <div className="h-8 bg-white/20 rounded w-1/2"></div>
      </div>
    </LoadingSkeleton>
  );
}

export function ChartSkeleton({ className = '' }: LoadingSkeletonProps) {
  return (
    <LoadingSkeleton className={`h-64 ${className}`}>
      <div className="flex items-center justify-center h-full">
        <div className="flex space-x-2">
          <div className="w-2 h-2 bg-white/30 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-white/30 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-white/30 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </LoadingSkeleton>
  );
}

export function HeatmapSkeleton({ className = '' }: LoadingSkeletonProps) {
  return (
    <div className={`space-y-4 ${className}`}>
      <div className="space-y-2">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="space-y-2">
            <div className="flex items-center gap-4">
              <div className="h-4 bg-white/20 rounded w-16"></div>
              <div className="flex-1 h-px bg-white/10"></div>
              <div className="h-3 bg-white/20 rounded w-20"></div>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {[...Array(30)].map((_, j) => (
                <div key={j} className="w-4 h-4 bg-white/10 rounded-md"></div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function TextSkeleton({ lines = 1, className = '' }: LoadingSkeletonProps & { lines?: number }) {
  return (
    <div className={`space-y-2 ${className}`}>
      {[...Array(lines)].map((_, i) => (
        <div 
          key={i} 
          className={`h-4 bg-white/20 rounded ${i === lines - 1 ? 'w-3/4' : 'w-full'}`}
        ></div>
      ))}
    </div>
  );
}

export function Spinner({ size = 'sm', className = '' }: { size?: 'sm' | 'md' | 'lg'; className?: string }) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6', 
    lg: 'w-8 h-8'
  };
  
  return (
    <div className={`animate-spin ${sizeClasses[size]} ${className}`}>
      <div className="h-full w-full border-2 border-white/20 border-t-white rounded-full"></div>
    </div>
  );
}

export function LoadingState({ message = 'Loading...', showSpinner = true }: { message?: string; showSpinner?: boolean }) {
  return (
    <div className="flex flex-col items-center justify-center py-8 space-y-3">
      {showSpinner && <Spinner size="md" />}
      <p className="text-sm text-zinc-400 animate-pulse">{message}</p>
    </div>
  );
}
