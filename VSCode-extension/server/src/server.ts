/* --------------------------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License. See License.txt in the project root for license information.
 * ------------------------------------------------------------------------------------------ */
import {
	createConnection,
	TextDocuments,
	Diagnostic,
	DiagnosticSeverity,
	ProposedFeatures,
	InitializeParams,
	DidChangeConfigurationNotification,
	CompletionItem,
	CompletionItemKind,
	TextDocumentPositionParams,
	TextDocumentSyncKind,
	InitializeResult
} from 'vscode-languageserver/node';


import {
	TextDocument
} from 'vscode-languageserver-textdocument';

import { execFileSync } from 'child_process';
import { TIMEOUT } from 'dns';
import { existsSync} from 'fs';

// Create a connection for the server, using Node's IPC as a transport.
// Also include all preview / proposed LSP features.
const connection = createConnection(ProposedFeatures.all);

// Create a simple text document manager.
const documents: TextDocuments<TextDocument> = new TextDocuments(TextDocument);

let hasConfigurationCapability = false;
let hasWorkspaceFolderCapability = false;
let hasDiagnosticRelatedInformationCapability = false;

connection.onInitialize((params: InitializeParams) => {
	const capabilities = params.capabilities;

	// Does the client support the `workspace/configuration` request?
	// If not, we fall back using global settings.
	hasConfigurationCapability = !!(
		capabilities.workspace && !!capabilities.workspace.configuration
	);
	hasWorkspaceFolderCapability = !!(
		capabilities.workspace && !!capabilities.workspace.workspaceFolders
	);
	hasDiagnosticRelatedInformationCapability = !!(
		capabilities.textDocument &&
		capabilities.textDocument.publishDiagnostics &&
		capabilities.textDocument.publishDiagnostics.relatedInformation
	);

	const result: InitializeResult = {
		capabilities: {
			textDocumentSync: TextDocumentSyncKind.Incremental,
			// Tell the client that this server supports code completion.
			completionProvider: {
				resolveProvider: true
			}
		}
	};
	if (hasWorkspaceFolderCapability) {
		result.capabilities.workspace = {
			workspaceFolders: {
				supported: true
			}
		};
	}
	return result;
});

connection.onInitialized(() => {
	if (hasConfigurationCapability) {
		// Register for all configuration changes.
		connection.client.register(DidChangeConfigurationNotification.type, undefined);
	}
	if (hasWorkspaceFolderCapability) {
		connection.workspace.onDidChangeWorkspaceFolders(_event => {
			connection.console.log('Workspace folder change event received.');
		});
	}
});

// The example settings
interface ExampleSettings {
	maxNumberOfProblems: number;
}

// The global settings, used when the `workspace/configuration` request is not supported by the client.
// Please note that this is not the case when using this server with the client provided in this example
// but could happen with other clients.
const defaultSettings: ExampleSettings = { maxNumberOfProblems: 1000 };
let globalSettings: ExampleSettings = defaultSettings;

// Cache the settings of all open documents
const documentSettings: Map<string, Thenable<ExampleSettings>> = new Map();

connection.onDidChangeConfiguration(change => {
	if (hasConfigurationCapability) {
		// Reset all cached document settings
		documentSettings.clear();
	} else {
		globalSettings = <ExampleSettings>(
			(change.settings.languageServerExample || defaultSettings)
		);
	}

	// Revalidate all open text documents
	documents.all().forEach(validateTextDocument);
});

function getDocumentSettings(resource: string): Thenable<ExampleSettings> {
	if (!hasConfigurationCapability) {
		return Promise.resolve(globalSettings);
	}
	let result = documentSettings.get(resource);
	if (!result) {
		result = connection.workspace.getConfiguration({
			scopeUri: resource,
			section: 'languageServerExample'
		});
		documentSettings.set(resource, result);
	}
	return result;
}

// Only keep settings for open documents
documents.onDidClose(e => {
	documentSettings.delete(e.document.uri);
});

// The content of a text document has changed. This event is emitted
// when the text document first opened or when its content has changed.

let complete : CompletionItem[];

function updateComplete(textDocument: TextDocument): void {
	complete = [
			{
				label: 'Alphabet',
				kind: CompletionItemKind.Text
			},
			{
				label: 'JavaScript',
				kind: CompletionItemKind.Text
			},
			{
				label: 'States',
				kind: CompletionItemKind.Text
			},
			{
				label: 'Function',
				kind: CompletionItemKind.Text
			},
			{
				label: 'Success',
				kind: CompletionItemKind.Text
			},
			{
				label: 'Fail',
				kind: CompletionItemKind.Text
			},
			{
				label: 'Start',
				kind: CompletionItemKind.Text
			},
			{
				label: 'Blank',
				kind: CompletionItemKind.Text
			},
			{
				label: 'left',
				kind: CompletionItemKind.Text
			},
			{
				label: 'right',
				kind: CompletionItemKind.Text
			},
			{
				label: 'stay',
				kind: CompletionItemKind.Text
			}
		];

		if (!existsSync('parser')){
			return;
		}
		const identefers = execFileSync('./parser', ['--identefers', '--text', textDocument.getText()]).toString('utf-8').split(' ');

		identefers.forEach((_s: string): void => {
			complete.push({
				label: _s,
				kind: CompletionItemKind.Text
			});
		});

}

documents.onDidChangeContent(change => {
	updateComplete(change.document);	
	validateTextDocument(change.document);
});


async function validateTextDocument(textDocument: TextDocument): Promise<void> {
	if (!existsSync('parser')){
		return;
	}
	// In this simple example we get the settings for every validate run.
	const settings = await getDocumentSettings(textDocument.uri);

	// The validator creates diagnostics for all uppercase words length 2 and more

	const text = textDocument.getText();
	const lines = execFileSync('./parser', ['--warnings', '--text', textDocument.getText()]).toString('utf-8').split('\n');

	const diagnostics: Diagnostic[] = [];
	for (let i = 0; i < lines.length; ++i){
		const line = lines[i].split(' ');
		if (line.length < 4) {
			continue;
		}
		const type = line[0];
		const numLine = parseInt(line[1]);
		const numPos = parseInt(line[2]);
		const len = parseInt(line[3]);
		const message = line[4].slice(1, -2);
		const diagnostic : Diagnostic = 			{
			severity: DiagnosticSeverity.Warning,
			range: {
				start: {line: numLine + 1, character: numPos},
				end: {line: numLine + 1, character: numPos + len}
			},
			message : message,
		};
		diagnostics.push(diagnostic);
	}

	// 	if (hasDiagnosticRelatedInformationCapability) {
	// 		diagnostic.relatedInformation = [
	// 			{
	// 				location: {
	// 					uri: textDocument.uri,
	// 					range: Object.assign({}, diagnostic.range)
	// 				},
	// 				message: diagnostic.message
	// 			}
	// 		];
	// 	}
	// 	diagnostics.push(diagnostic);
	// }

	// Send the computed diagnostics to VSCode.
	connection.sendDiagnostics({ uri: textDocument.uri, diagnostics });
}

connection.onDidChangeWatchedFiles(_change => {
	// Monitored files have change in VSCode
	connection.console.log('We received an file change event');
});


// This handler provides the initial list of the completion items.
connection.onCompletion(
	(_textDocument: TextDocumentPositionParams): CompletionItem[] => {
		// The pass parameter contains the position of the text document in
		// which code complete got requested. For the example we ignore this
		// info and always provide the same completion items.

		return complete;
	}
);

// This handler resolves additional information for the item selected in
// the completion list.
connection.onCompletionResolve(
	(item: CompletionItem): CompletionItem => {
		return item;
	}
);

// Make the text document manager listen on the connection
// for open, change and close text document events
documents.listen(connection);

// Listen on the connection
connection.listen();
