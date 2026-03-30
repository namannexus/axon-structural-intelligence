import React, { useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Sky } from '@react-three/drei';

const Wall = ({ start, end, type }) => {
  const dx = end.x - start.x;
  const dz = end.y - start.y;
  const length = Math.sqrt(dx * dx + dz * dz);
  const angle = Math.atan2(dz, dx);
  const height = 300;
  const thickness = type === 'load-bearing' ? 12 : 8;

  return (
    <mesh position={[(start.x + end.x)/2, height/2, (start.y + end.y)/2]} rotation={[0, -angle, 0]}>
      <boxGeometry args={[length, height, thickness]} />
      <meshStandardMaterial color={type === 'load-bearing' ? '#d32f2f' : '#1976d2'} />
    </mesh>
  );
};

export default function FloorPlan3D({ graphData }) {
  if (!graphData) return null;

  return (
    <div className="w-full h-full relative bg-slate-900">
      <Canvas camera={{ position: [0, 1000, 1000], fov: 45 }}>
        <Sky sunPosition={[100, 20, 100]} />
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 20, 10]} intensity={1} />
        
        <group position={[-500, 0, -500]}>
          {graphData.edges.map((edge, i) => (
            <Wall 
              key={i} 
              start={graphData.nodes.find(n => n.id === edge.source)} 
              end={graphData.nodes.find(n => n.id === edge.target)} 
              type={graphData.wall_types[edge.wall_id]} 
            />
          ))}
        </group>
        <OrbitControls makeDefault />
      </Canvas>
    </div>
  );
}