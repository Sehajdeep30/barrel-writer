<template>
	
	<div
		style="box-shadow: none;"
		v-for="msg in session_history"
	>
		<p style="display: inline;"> {{ msg["prompt"] }}</p>
		<mark style="display: inline;">{{ msg["completion"] }}</mark>
		<br><br>
	</div>

	<div>
		<div>
			<textarea id="text-input" v-model="prompt_text">
			</textarea>
		</div>

		<div class="grid">
			<select id="model" required v-model="model_type">
				<option value="" selected>select a model</option>
				<option value="scifi">SciFi and Sepculative Fiction</option>
  				<option value="philosophy">Philosophy</option>
  				<option value="academia">Academia</option>
			</select>

			<label for="output-length">Output Length (10-100 chars)
				<input
					type="range"
					min="10" max="100"
					id="range"
					v-model="generation_length">
			</label>

			<button class="outline" @click="fetch_suggestion()">get suggestion</button>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			session_history: [
				{
					"prompt": "prompt 1",
					"completion": "completion 1"
				}
			],

			prompt_text: "",
			generation_length: 50,
			model_type: ""
		}
	},

	methods: {
		print_values() {
			console.log("https://1409-157-37-189-118.in.ngrok.io/"+this.model_type +'/'+this.generation_length+'/'+this.prompt_text)
		},
		
		async fetch_completion() {
			const response = await fetch("https://1409-157-37-189-118.in.ngrok.io/"+this.model_type +'/'+this.generation_length+'/'+this.prompt_text).then((res) => res.json())
			console.log(response)
			this.session_history.push(response);
		},

		fetch_suggestion() {
			var xmlHttp = new XMLHttpRequest();
			xmlHttp.open(
				"GET",
				"https://1409-157-37-189-118.in.ngrok.io/"+this.model_type +'/'+this.generation_length+'/'+this.prompt_text,
				false
			); // false for synchronous request
    		xmlHttp.send( null );
			console.log(JSON.parse(xmlHttp.responseText))
    		this.session_history.push(JSON.parse(xmlHttp.responseText))
		}
	},

	mounted() {
	/*
		const input_element = new SimpleMDE({
			element: document.getElementById("text-input"),
			autosave: {
				enabled: true,
				uniqueId: "simpleMDE_autosave_data",
				delay: 1000,
			},
			spellChecker: false,
			toolbar: false,
			status: false,
			placeholder: "Type here..."
		})
	*/
	}

}
</script>

<style scoped>
</style>
