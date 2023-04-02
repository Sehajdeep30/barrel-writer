<template>
	<div>
		<nav>
			<ul>
				<li><strong>barrel</strong></li>
			</ul>
			<ul>
			    <li><button class="secondary outline" @click="toggleSettingsDialog()">settings</button></li>
			    <li><a href="https://github.com/s-m33r/barrel-writer">source</a></li>
			    <li><a href="#">about</a></li>
			</ul>
		</nav>
	</div>

	<section>
		<div
			style="box-shadow: none;"
			v-for="msg in session_history"
		>
			<p style="display: inline;"> {{ msg["prompt"] }}</p>
			<mark style="display: inline;">{{ msg["completion"].slice(msg["prompt"].length + 1) }}</mark>
			<br><br>
		</div>
	</section>

	<dialog open v-show="display_settings_page">

		<article>
			<a class="close" @click="toggleSettingsDialog()"></a>

			<select id="model" required v-model="model_type">
				<option value="" selected>select a model</option>
  				<option value="litreature">Literary</option>
				<option value="scifi">SciFi and Speculative Fiction</option>
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
		</article>

	</dialog>

	<div style="position: sticky; bottom: 0;">
		<div @keydown.alt.enter="status_waiting_for_response = !status_waiting_for_response; fetch_completion()">
			<textarea id="text-input" v-model="prompt_text">
			</textarea>
		</div>
		
		<progress v-show="status_waiting_for_response"></progress>
		<button class="secondary outline"
			@click="status_waiting_for_response = !status_waiting_for_response; fetch_completion()"
			v-show="!status_waiting_for_response"
		>get suggestion</button>
	</div>

</template>

<script>
export default {
	data() {
		return {
			display_settings_page: false,

			status_waiting_for_response: false,

			session_history: [],

			prompt_text: "",
			generation_length: 50,
			model_type: "",
		}
	},

	methods: {
		toggleSettingsDialog() {
			this.display_settings_page = !this.display_settings_page
		},

		toggleBoolStatus(status) {
			this[status] = !this[status]
		},
		
		async fetch_completion() {
			if (this.input_element.value() == "" || this.model_type == "") {
				this.status_waiting_for_response = false
				return
			}

			const request = new Request("http://localhost:8000/", {
				method: "POST",
				body: JSON.stringify({
					"model": this.model_type,
					"length": parseInt(this.generation_length),
					"prompt": this.input_element.value()
				})
			});

			const response = await fetch(request)

			this.session_history.push(await response.json())

			this.status_waiting_for_response = false
		}

	},

	mounted() {
		this.input_element = new SimpleMDE({
			autofocus: true,
			element: document.getElementById("text-input"),
			autosave: {
				enabled: true,
				uniqueId: "simpleMDE_autosave_data",
				delay: 1000,
			},
			spellChecker: false,
			toolbar: false,
			status: false,

			placeholder: "Type here...\nPress Alt+Enter to get a suggestion (or click the button below)"
		})
	}

}
</script>

<style>
/* minimum height of editor (SimpleMDE) */
.CodeMirror, .CodeMirror-scroll {
	min-height: 100px;
}
</style>
