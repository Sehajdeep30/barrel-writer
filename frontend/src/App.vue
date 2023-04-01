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

			<button class="outline" @click="fetch_completion()">get suggestion</button>
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
		
		async fetch_completion() {
			api_endpoint = "https://64a6-2405-204-1483-d13d-52d4-d327-cff0-c84c.in.ngrok.io "
			const request = new Request(api_endpoint, {
				method: "GET",
				body: JSON.stringify({
					"model": this.model_type,
					"length": this.generation_length,
					"text": this.prompt_text
				})
			});


			const response = await fetch(request)

			console.log(response)
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
