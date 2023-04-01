<template>

	<form>
		<div class="grid">
			<select id="model" required v-model="model">
				<option value="" selected>select a model</option>
				<option value="scifi-speculative">SciFi and Sepculative Fiction</option>
  				<option value="poetry">Poetry</option>
			</select>

			<label for="output-length">Output Length (10-100 chars)
				<input
					type="range"
					min="10" max="100"
					id="range" name="range"
					v-model="generation_length">
			</label>

			<button class="outline">get suggestion</button>
		</div>
	</form>

	<textarea id="text-input" v-model="text">
	</textarea>

</template>

<script>
export default {
	data() {
		return {
			text: "",
			generation_length: 50,
			model: ""
		}
	},

	mounted() {
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
	}
}
</script>
