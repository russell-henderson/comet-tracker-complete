// frontend/src/components/CometTracker.jsx
import React from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  Telescope,
  MapPin,
  Zap,
  Eye,
  Star,
  Orbit,
  RefreshCw,
  Clock,
  Calendar,
} from "lucide-react";

import CometProximityVisualization from "./CometProximityVisualization";
import SkyLiveEmbedCard from "./SkyLiveEmbedCard";
import CountdownPill from "./CountdownPill";

export default function CometTracker({
  cometData,
  error,
  isLoading = false,
  fetchCometData,
}) {
  const handleRefresh =
    typeof fetchCometData === "function" ? fetchCometData : () => {};

  const closestApproachISO =
    cometData?.events?.closestApproach?.timestamp ||
    process.env.REACT_APP_CLOSEST_APPROACH;

  const formatTime = (iso) => {
    try {
      return new Date(iso).toLocaleString();
    } catch {
      return "N/A";
    }
  };

  const lastUpdatedISO =
    cometData?.updatedAt || cometData?.timestamp || new Date().toISOString();

  const nextUpdateISO =
    cometData?.nextUpdate ||
    new Date(Date.now() + 15 * 60 * 1000).toISOString();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Header */}
      <div className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Left: title */}
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-500/20 rounded-lg">
                <Telescope className="h-6 w-6 text-blue-400" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Comet 3i/Atlas Tracker</h1>
                <p className="text-slate-400 text-sm">
                  Real-time astronomical monitoring
                </p>
              </div>
            </div>

            {/* Right: countdown + error + refresh */}
            <div className="flex items-center gap-4">
              {error && (
                <div className="hidden md:block text-sm text-red-400 max-w-[22rem] truncate">
                  {error}
                </div>
              )}
              <CountdownPill
                targetISO={closestApproachISO}
                label="Closest approach"
              />
              <Button
                variant="outline"
                size="sm"
                onClick={handleRefresh}
                disabled={isLoading}
                className="border-slate-600 hover:bg-slate-700"
              >
                <RefreshCw
                  className={`h-4 w-4 mr-2 ${isLoading ? "animate-spin" : ""}`}
                />
                Refresh
              </Button>
            </div>
          </div>

          {/* Mobile error */}
          {error && (
            <div className="mt-2 md:hidden text-sm text-red-400 truncate">
              {error}
            </div>
          )}
        </div>
      </div>

      {/* Main content */}
      <div className="container mx-auto px-6 py-8">
        {/* Proximity Visualization */}
        <div className="mb-8">
          <CometProximityVisualization cometData={cometData} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">
          {/* Left column */}
          <div className="lg:col-span-2 flex flex-col gap-6 h-full">
            {/* Current Position */}
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center space-x-2">
                    <MapPin className="h-5 w-5 text-blue-400" />
                    <span>Current Position</span>
                  </CardTitle>
                  <Badge
                    variant="secondary"
                    className="bg-slate-700 text-slate-200"
                  >
                    Live Data
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <p className="text-sm text-slate-400">Right Ascension</p>
                    <p className="text-2xl font-mono text-blue-400">
                      {cometData?.position?.rightAscension}°
                    </p>
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm text-slate-400">Declination</p>
                    <p className="text-2xl font-mono text-blue-400">
                      {cometData?.position?.declination}°
                    </p>
                  </div>
                </div>

                <Separator className="bg-slate-700" />

                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <p className="text-sm text-slate-400">Distance from Earth</p>
                    <p className="text-xl font-mono text-green-400">
                      {cometData?.position?.distance} AU
                    </p>
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm text-slate-400">Distance from Sun</p>
                    <p className="text-xl font-mono text-orange-400">
                      {cometData?.position?.heliocentricDistance} AU
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Velocity & Movement */}
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Zap className="h-5 w-5 text-yellow-400" />
                  <span>Velocity & Movement</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <p className="text-sm text-slate-400">Radial Velocity</p>
                    <p className="text-xl font-mono text-yellow-400">
                      {cometData?.velocity?.radialVelocity} km/s
                    </p>
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm text-slate-400">Tangential Velocity</p>
                    <p className="text-xl font-mono text-yellow-400">
                      {cometData?.velocity?.tangentialVelocity} km/s
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* 3D View embed fills remaining height */}
            <SkyLiveEmbedCard aspectPercent={62} />
          </div>

          {/* Right column */}
          <div className="space-y-6">
            {/* Visibility */}
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Eye className="h-5 w-5 text-purple-400" />
                  <span>Visibility</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm text-slate-400">Constellation</p>
                  <p className="text-lg font-semibold text-purple-400">
                    {cometData?.visibility?.constellation}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Best Viewing</p>
                  <p className="text-sm text-slate-200">
                    {cometData?.visibility?.bestViewingTime}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Moon Phase</p>
                  <p className="text-sm text-slate-200">
                    {cometData?.visibility?.moonPhase}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Physical Data */}
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Star className="h-5 w-5 text-amber-400" />
                  <span>Physical Data</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm text-slate-400">Magnitude</p>
                  <p className="text-lg font-mono text-amber-400">
                    {cometData?.physical?.magnitude}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Coma Diameter</p>
                  <p className="text-sm text-slate-200">
                    {cometData?.physical?.coma}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Tail Length</p>
                  <p className="text-sm text-slate-200">
                    {cometData?.physical?.tail}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Orbital Elements */}
            <Card className="bg-slate-800/50 border-slate-700">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Orbit className="h-5 w-5 text-cyan-400" />
                  <span>Orbital Elements</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm text-slate-400">Eccentricity</p>
                  <p className="text-sm font-mono text-cyan-400">
                    {cometData?.orbital?.eccentricity}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Inclination</p>
                  <p className="text-sm font-mono text-cyan-400">
                    {cometData?.orbital?.inclination}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Perihelion</p>
                  <p className="text-sm text-slate-200">
                    {cometData?.orbital?.perihelion}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Period</p>
                  <p className="text-sm text-slate-200">
                    {cometData?.orbital?.period}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 flex flex-col md:flex-row md:items-center md:justify-between text-sm text-slate-400 gap-2">
          <div className="flex items-center flex-wrap gap-x-6 gap-y-2">
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4" />
              <span>Last updated: {formatTime(lastUpdatedISO)}</span>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              <span>Next update: {formatTime(nextUpdateISO)}</span>
            </div>
          </div>
          <div className="text-xs">
            Data source: {cometData?.source || "NASA JPL Horizons"} • Updates
            every 15 minutes
          </div>
        </div>
      </div>
    </div>
  );
}
