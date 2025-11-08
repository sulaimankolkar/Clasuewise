import React from 'react'
import { useFrame } from '@react-three/fiber'
import { useRef } from 'react'

function Scene3D() {
  const groupRef = useRef()

  useFrame(() => {
    if (groupRef.current) {
      groupRef.current.rotation.x += 0.0001
      groupRef.current.rotation.y += 0.0002
    }
  })

  return (
    <>
      <color attach="background" args={['#0f1419']} />
      <fog attach="fog" args={['#0f1419', 5, 15]} />

      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1.5} />
      <pointLight position={[-10, -10, -5]} intensity={0.5} color="#6366f1" />

      <group ref={groupRef}>
        <mesh position={[-3, 0, -5]}>
          <octahedronGeometry args={[1, 0]} />
          <meshPhongMaterial color="#6366f1" wireframe opacity={0.3} />
        </mesh>

        <mesh position={[3, 0, -5]}>
          <tetrahedronGeometry args={[1.2, 0]} />
          <meshPhongMaterial color="#818cf8" wireframe opacity={0.3} />
        </mesh>

        <mesh position={[0, 2, -6]}>
          <icosahedronGeometry args={[0.8, 0]} />
          <meshPhongMaterial color="#a78bfa" wireframe opacity={0.3} />
        </mesh>
      </group>

      <mesh position={[0, -2, -8]} scale={20}>
        <planeGeometry />
        <meshStandardMaterial color="#1a1f2e" />
      </mesh>
    </>
  )
}

export default Scene3D
