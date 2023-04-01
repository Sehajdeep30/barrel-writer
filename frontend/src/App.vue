<template>
	
	<article
		style="box-shadow: none;"
		v-for="msg in session_history"
	>
		<header>user text</header>
		<body>{{ msg.message }}</body>
	</article>

	<InputBox />
</template>

<script>
import InputBox from "./components/InputBox.vue"

export default {
	components: {
		InputBox
	},

	data() {
		return {
			session_history: []
		}
	},

	mounted() {
    var pusher = new Pusher('api-key', {
      cluster: 'ap2'
    });

    var channel = pusher.subscribe('my-channel');
    channel.bind('my-event', function(data) {
      alert(JSON.stringify(data));
			this.session_history.push(data);
    });
	}

}
</script>

<style scoped>
</style>
