/* Optional local fixture checks. No SAP connection or desktop interaction.
 * From the repository root:
 * pnpm exec node skills/sap-gui-scripting/scripts/validate-scripts.cjs
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const inspectSource = fs.readFileSync(path.join(__dirname, 'inspect-session.js'), 'utf8');
const smokeSource = fs.readFileSync(path.join(__dirname, 'se16-table-smoke.js'), 'utf8');
const target = {systemName: 'TEST', client: '001', user: 'FIXTURE', sessionId: ''};
const collection = items => ({length: items.length, elementAt: index => items[index]});

function fixture(options = {}) {
    const actions = [];
    const info = {
        ...target, transaction: options.transaction || 'SESSION_MANAGER',
        program: 'SAPLSMTR_NAVIGATION', screenNumber: '100',
        scriptingModeReadOnly: !!options.readOnly,
        scriptingModeRecordingDisabled: false,
    };
    let tableName = '';
    let maxRows = '1000';
    const status = {messageType: '', text: ''};
    const session = {
        id: '/app/con[0]/ses[0]', info,
        activeWindow: {type: options.modal ? 'GuiModalWindow' : 'GuiMainWindow'},
        startTransaction(code) {
            actions.push(['start', code]);
            info.transaction = code;
            info.program = 'SAPLSETB';
            info.screenNumber = '100';
        },
        findById(id) {
            if (id === 'wnd[0]/usr/ctxtDATABROWSE-TABLENAME') {
                if (options.missingTableField) throw new Error('Control not found');
                return {
                    get text() { return tableName; },
                    set text(value) { tableName = value; actions.push(['table', value]); },
                };
            }
            if (id === 'wnd[0]/usr/txtMAX_SEL') return {
                get text() { return maxRows; },
                set text(value) {
                    actions.push(['limit', value]);
                    if (!options.rejectLimit) maxRows = value;
                },
            };
            if (id === 'wnd[0]/sbar') return status;
            if (id === 'wnd[0]') return {
                sendVKey(key) {
                    actions.push(['key', key]);
                    if (key === 0) {
                        info.program = options.wrongProgram ? 'OTHER' : '/1BCDWB/DB' + tableName;
                        info.screenNumber = '1000';
                        if (options.tableDenied) Object.assign(status, {messageType: 'E', text: 'Not authorized'});
                    }
                    if (key === 8) {
                        assert.equal(maxRows, '10', 'The cap must precede execution');
                        if (!options.stayOnSelection) {
                            info.program = 'SAPLSLVC_FULLSCREEN';
                            info.screenNumber = '500';
                        }
                        if (options.queryError) Object.assign(status, {messageType: 'E', text: 'Query failed'});
                    }
                },
            };
            throw new Error('Unexpected control: ' + id);
        },
    };
    const otherSession = {...session, id: '/app/con[0]/ses[1]'};
    const connection = {id: '/app/con[0]', children: collection(options.noSession ? [] : options.duplicate ? [session, otherSession] : [session])};
    return {actions, session, application: {children: collection([connection])}};
}

function executeSmoke(state, configuration = {}) {
    const source = smokeSource
        .replace('var SAP_GUI_TARGET = {systemName: "", client: "", user: "", sessionId: ""};',
            'var SAP_GUI_TARGET = ' + JSON.stringify(configuration.target || target) + ';')
        .replace('var SAP_GUI_EXECUTE = false;', 'var SAP_GUI_EXECUTE = ' + JSON.stringify(configuration.execute ?? false) + ';')
        .replace('var SAP_GUI_MAX_ROWS = 10;', 'var SAP_GUI_MAX_ROWS = ' + JSON.stringify(configuration.maxRows ?? 10) + ';');
    return JSON.parse(vm.runInNewContext(source, {application: state.application}));
}

let passed = 0;
function test(name, run) {
    run();
    passed++;
    process.stdout.write('PASS ' + name + '\n');
}

test('Missing SAP host cannot run inspection', () => {
    assert.throws(() => vm.runInNewContext(inspectSource, {}), /SAP GUI for Java/);
});
test('Inspection returns metadata without navigation', () => {
    const state = fixture();
    const result = JSON.parse(vm.runInNewContext(inspectSource, {application: state.application}));
    assert.equal(result.sessions.length, 1);
    assert.equal(result.sessions[0].systemName, 'TEST');
    assert.equal(result.errors.length, 0);
    assert.deepEqual(state.actions, []);
});
test('Inspection surfaces inaccessible connections', () => {
    const application = {children: collection([{get children() { throw new Error('Access denied'); }}])};
    const result = JSON.parse(vm.runInNewContext(inspectSource, {application}));
    assert.equal(result.sessions.length, 0);
    assert.match(result.errors[0].error, /Access denied/);
});
test('Unconfigured shipped smoke script refuses navigation', () => {
    const state = fixture();
    assert.throws(() => vm.runInNewContext(smokeSource, {application: state.application}), /Configure/);
    assert.deepEqual(state.actions, []);
});
for (const [name, options, config, error] of [
    ['Missing session', {noSession: true}, {}, /found 0/],
    ['Ambiguous sessions', {duplicate: true}, {}, /found 2/],
    ['Wrong identity even with a session ID', {}, {target: {...target, user: 'OTHER', sessionId: '/app/con[0]/ses[0]'}}, /found 0/],
    ['Read-only scripting', {readOnly: true}, {}, /read-only/],
    ['Unexpected modal', {modal: true}, {}, /modal/],
    ['Unrelated transaction', {transaction: 'VA02'}, {}, /Easy Access/],
    ['Unbounded cap rejected', {}, {execute: true, maxRows: 0}, /row cap/],
    ['Invalid execute option', {}, {execute: 'true'}, /boolean/],
]) test(name + ' stops before navigation', () => {
    const state = fixture(options);
    assert.throws(() => executeSmoke(state, config), error);
    assert.deepEqual(state.actions, []);
});
test('Explicit session ID resolves an ambiguous identity', () => {
    const state = fixture({duplicate: true});
    assert.equal(executeSmoke(state, {target: {...target, sessionId: state.session.id}}).phase, 'selection');
});
test('Selection-only mode never executes a query', () => {
    const state = fixture();
    const result = executeSmoke(state);
    assert.equal(result.phase, 'selection');
    assert.equal(result.program, '/1BCDWB/DBVBAK');
    assert.equal(result.maxRows, null);
    assert.deepEqual(state.actions, [['start', 'SE16'], ['table', 'VBAK'], ['key', 0]]);
});
for (const [name, options, error] of [
    ['Missing control', {missingTableField: true}, /Control not found/],
    ['Table authorization failure', {tableDenied: true}, /Not authorized/],
    ['Wrong selection program', {wrongProgram: true}, /selection program/],
    ['Unapplied result cap', {rejectLimit: true}, /limit was not applied/],
]) test(name + ' prevents query execution', () => {
    const state = fixture(options);
    assert.throws(() => executeSmoke(state, {execute: true}), error);
    assert.ok(!state.actions.some(([kind, value]) => kind === 'key' && value === 8));
});
test('Bounded read executes once after applying its cap', () => {
    const state = fixture();
    const result = executeSmoke(state, {execute: true});
    assert.equal(result.phase, 'query_completed');
    assert.equal(result.maxRows, 10);
    assert.equal(result.program, 'SAPLSLVC_FULLSCREEN');
    assert.deepEqual(state.actions.slice(-2), [['limit', '10'], ['key', 8]]);
});
for (const options of [{queryError: true}, {stayOnSelection: true}]) test('Failed query is reported without retry', () => {
    const state = fixture(options);
    assert.throws(() => executeSmoke(state, {execute: true}), /Query did not reach/);
    assert.equal(state.actions.filter(([kind, value]) => kind === 'key' && value === 8).length, 1);
});
process.stdout.write(passed + ' local fixture checks passed; no live SAP connection used.\n');
