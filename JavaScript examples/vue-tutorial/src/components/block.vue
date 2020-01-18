<template>
  <div id  = "ComponentB">
    <p v-rect :config="{
        x: 20,
        y: 50,
        width: 100,
        height: 100, 
        fill: 'red',
        shadowBlur: 10
        }"
        />

    </div>
</template>