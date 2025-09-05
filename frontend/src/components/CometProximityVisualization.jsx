import React from 'react';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Globe, 
  Target, 
  ArrowRight,
  Telescope,
  MapPin
} from 'lucide-react';

const CometProximityVisualization = ({ cometData }) => {
  // Calculate proximity level based on distance
  const getProximityLevel = (distance) => {
    const dist = parseFloat(distance);
    if (dist < 1) return { level: 'Very Close', color: 'bg-red-500', intensity: 'high' };
    if (dist < 2) return { level: 'Close', color: 'bg-orange-500', intensity: 'medium-high' };
    if (dist < 5) return { level: 'Moderate', color: 'bg-yellow-500', intensity: 'medium' };
    if (dist < 10) return { level: 'Distant', color: 'bg-blue-500', intensity: 'low-medium' };
    return { level: 'Very Distant', color: 'bg-slate-500', intensity: 'low' };
  };

  const proximity = cometData ? getProximityLevel(cometData.position?.distance) : { level: 'Unknown', color: 'bg-slate-500', intensity: 'low' };

  const getTrajectoryAnimation = (intensity) => {
    const speeds = {
      'high': 'animate-ping',
      'medium-high': 'animate-pulse',
      'medium': 'animate-bounce',
      'low-medium': '',
      'low': ''
    };
    return speeds[intensity] || '';
  };

  return (
    <Card className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border-slate-700 overflow-hidden">
      <div className="relative">
        {/* Hero Background Image */}
        <div 
          className="absolute inset-0 bg-cover bg-center opacity-30"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1594270027562-c3c194953212?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwzfHxlYXJ0aCUyMGNvbWV0JTIwc3BhY2V8ZW58MHx8fHwxNzU3MDY0NDc5fDA&ixlib=rb-4.1.0&q=85')`
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-r from-slate-900/80 via-slate-800/60 to-slate-900/80" />
        
        <CardContent className="relative p-8">
          <div className="flex items-center justify-between">
            {/* Left side - Earth representation */}
            <div className="flex items-center space-x-6">
              <div className="relative">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-700 rounded-full flex items-center justify-center shadow-lg">
                  <Globe className="h-10 w-10 text-white" />
                </div>
                <div className="absolute -top-2 -right-2">
                  <div className="w-4 h-4 bg-green-400 rounded-full animate-pulse" />
                </div>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-white">Earth</h3>
                <p className="text-slate-300 text-sm">Observer Location</p>
                <Badge variant="secondary" className="mt-1 bg-blue-500/20 text-blue-300">
                  Reference Point
                </Badge>
              </div>
            </div>

            {/* Middle - Distance and trajectory */}
            <div className="flex-1 flex flex-col items-center space-y-4 mx-8">
              <div className="flex items-center space-x-2 text-slate-400">
                <div className="flex-1 h-px bg-gradient-to-r from-transparent via-slate-500 to-transparent" />
                <ArrowRight className="h-5 w-5" />
                <div className="flex-1 h-px bg-gradient-to-r from-transparent via-slate-500 to-transparent" />
              </div>
              
              <div className="text-center">
                <div className="text-2xl font-mono text-white mb-1">
                  {cometData?.position?.distance || '4.20000000'} <span className="text-sm text-slate-400">AU</span>
                </div>
                <div className="text-sm text-slate-300">Current Distance</div>
                <Badge 
                  className={`mt-2 ${proximity.color} text-white`}
                >
                  {proximity.level} Proximity
                </Badge>
              </div>

              <div className="flex items-center space-x-1">
                <div className={`w-2 h-2 rounded-full ${proximity.color} ${getTrajectoryAnimation(proximity.intensity)}`} />
                <div className={`w-1 h-1 rounded-full ${proximity.color} ${getTrajectoryAnimation(proximity.intensity)}`} style={{animationDelay: '0.1s'}} />
                <div className={`w-1 h-1 rounded-full ${proximity.color} ${getTrajectoryAnimation(proximity.intensity)}`} style={{animationDelay: '0.2s'}} />
              </div>
            </div>

            {/* Right side - Comet representation */}
            <div className="flex items-center space-x-6">
              <div>
                <h3 className="text-lg font-semibold text-white text-right">3i/Atlas Comet</h3>
                <p className="text-slate-300 text-sm text-right">{cometData?.designation || 'C/2025 A1'}</p>
                <div className="flex justify-end mt-1">
                  <Badge variant="secondary" className="bg-purple-500/20 text-purple-300">
                    Active Tracking
                  </Badge>
                </div>
              </div>
              
              <div className="relative">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center shadow-lg">
                  <Target className="h-10 w-10 text-white" />
                </div>
                <div className="absolute -top-2 -left-2">
                  <div className={`w-4 h-4 ${proximity.color} rounded-full ${getTrajectoryAnimation(proximity.intensity)}`} />
                </div>
                {/* Comet tail effect */}
                <div className="absolute top-1/2 -right-8 transform -translate-y-1/2">
                  <div className="w-8 h-1 bg-gradient-to-r from-purple-400 to-transparent opacity-60" />
                  <div className="w-6 h-px bg-gradient-to-r from-purple-300 to-transparent opacity-40 mt-1" />
                </div>
              </div>
            </div>
          </div>

          {/* Bottom stats row */}
          <div className="mt-8 pt-6 border-t border-slate-700">
            <div className="grid grid-cols-3 gap-6 text-center">
              <div>
                <div className="flex items-center justify-center space-x-2 mb-2">
                  <Telescope className="h-4 w-4 text-blue-400" />
                  <span className="text-sm font-medium text-slate-300">Visibility</span>
                </div>
                <div className="text-lg font-mono text-blue-400">
                  {cometData?.visibility?.constellation || 'Draco'}
                </div>
                <div className="text-xs text-slate-400">Constellation</div>
              </div>
              
              <div>
                <div className="flex items-center justify-center space-x-2 mb-2">
                  <MapPin className="h-4 w-4 text-yellow-400" />
                  <span className="text-sm font-medium text-slate-300">Velocity</span>
                </div>
                <div className="text-lg font-mono text-yellow-400">
                  {cometData?.velocity?.radialVelocity || '12.500'} km/s
                </div>
                <div className="text-xs text-slate-400">Radial Speed</div>
              </div>
              
              <div>
                <div className="flex items-center justify-center space-x-2 mb-2">
                  <Target className="h-4 w-4 text-purple-400" />
                  <span className="text-sm font-medium text-slate-300">Magnitude</span>
                </div>
                <div className="text-lg font-mono text-purple-400">
                  {cometData?.physical?.magnitude || '9.2'}
                </div>
                <div className="text-xs text-slate-400">Brightness</div>
              </div>
            </div>
          </div>
        </CardContent>
      </div>
    </Card>
  );
};

export default CometProximityVisualization;