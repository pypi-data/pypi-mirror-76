# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

_G='tested?'
_F='$0$'
_E='device'
_D='wn-sztpd-0:device'
_C='/'
_B='activation-code'
_A=None
import gc,tracemalloc,os,re,json,signal,asyncio,datetime,functools,pkg_resources
from .  import yl
from .dal import DataAccessLayer
from .rcsvr import RestconfServer
from passlib.hash import sha256_crypt
from .tenant import TenantViewHandler
from .rfc8572 import RFC8572ViewHandler
from .native import NativeViewHandler,Period,TimeUnit
loop=_A
sig=_A
def signal_handler(name):global loop;global sig;sig=name;loop.stop()
def run(db_url,cacert_param=_A,cert_param=_A,key_param=_A):
	f=':transport';e='SIGHUP';d='0';c=True;W='use-for';V='x';U='1';N=db_url;K=key_param;J=cert_param;I=cacert_param;E='';global loop;global sig;A=_A;B=_A;R=False
	if I is not _A and N.startswith('sqlite:'):print('The "sqlite" dialect does not support the "cacert" parameter.');return 1
	if(J or K)and not I:print('The "cacert" parameter must be specified whenever the "key" and "cert" parameters are specified.');return 1
	if(J is _A)!=(K is _A):print('The "key" and "cert" parameters must be specified together.');return 1
	try:A=DataAccessLayer(N,I,J,K)
	except (SyntaxError,AssertionError)as O:return 1
	except NotImplementedError as O:R=c
	else:B=A.opaque()
	if R==c:
		L=os.environ.get('SZTPD_MODE')
		if L!=_A:
			assert type(L)==str
			if L not in[d,U,V]:print('Unknown SZTPD_MODE value.  Must be 0, 1, or x.');return 1
			B=L
		else:
			print(E);X=pkg_resources.resource_filename('sztpd','LICENSE.txt');S=open(X,'r');print(S.read());S.close();print('First time initialization.  Please accept the license terms.');print(E);print('By entering "Yes" below, you agree to be bound to the terms and conditions contained on this screen with Watsen Networks.');print(E);Y=input('Please enter "Yes" or "No": ')
			if Y!='Yes':print(E);print('Thank you for your consideration.');print(E);return 1
			print(E);print('Modes:');print('  1 - single-tenant');print('  x - multi-tenant');print(E);B=input('Please select mode: ')
			if B not in[U,V]:print('Unknown mode selection.  Please try again.');return 1
			print(E);print("Running SZTPD in mode '"+B+"'. (No more output expected)");print(E)
		try:A=DataAccessLayer(N,I,J,K,json.loads(getattr(yl,'nbi_'+B)()),'wn-sztpd-'+B,B)
		except Exception as O:raise O;return 1
	assert B!=_A;assert A!=_A;tracemalloc.start(25);loop=asyncio.get_event_loop();loop.add_signal_handler(signal.SIGHUP,functools.partial(signal_handler,name=e));loop.add_signal_handler(signal.SIGTERM,functools.partial(signal_handler,name='SIGTERM'));loop.add_signal_handler(signal.SIGINT,functools.partial(signal_handler,name='SIGINT'));loop.add_signal_handler(signal.SIGQUIT,functools.partial(signal_handler,name='SIGQUIT'))
	while sig is _A:
		M=[];F=A.handle_get_config_request(_C+A.app_ns+f);P=loop.run_until_complete(F)
		for D in P[A.app_ns+f]['listen']['endpoint']:
			if D[W][0]=='native-interface':
				C=NativeViewHandler(A,B,loop)
				if B==d:G=_C+A.app_ns+':device'
				elif B==U:G=_C+A.app_ns+':devices/device'
				elif B==V:G=_C+A.app_ns+':tenants/tenant/devices/device'
				C.register_create_callback(G,_handle_device_created);Z=G+'/activation-code';C.register_change_callback(Z,_handle_device_act_code_changed);C.register_subtree_change_callback(G,_handle_device_subtree_changed);C.register_somehow_change_callback(G,_handle_device_somehow_changed);C.register_delete_callback(G,_handle_device_deleted);C.register_periodic_callback(Period(24,TimeUnit.Hours),datetime.datetime(2000,1,1,0),_check_expirations);Q=RestconfServer(loop,A,D,C)
			elif D[W][0]=='tenant-interface':a=TenantViewHandler(C);Q=RestconfServer(loop,A,D,a)
			else:assert D[W][0]=='rfc8572-interface';T=json.loads(getattr(yl,'sbi_rfc8572')());b=RFC8572ViewHandler(A,B,T,C);Q=RestconfServer(loop,A,D,b,T)
			M.append(Q);del D;D=_A
		del P;P=_A;loop.run_forever()
		for H in M:F=H.app.shutdown();loop.run_until_complete(F);F=H.runner.cleanup();loop.run_until_complete(F);F=H.app.cleanup();loop.run_until_complete(F);del H;H=_A
		del M;M=_A
		if sig==e:sig=_A
	loop.close();del A;return 0
async def _handle_device_created(watched_node_path,jsob,jsob_data_path,nvh):
	B=jsob;assert type(B)==dict
	if jsob_data_path==_C:assert _D in B;A=B[_D]
	else:assert _E in B;A=B[_E]
	A['lifecycle-statistics']={'nbi-access-stats':{'created':datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),'num-times-modified':0},'sbi-access-stats':{'num-times-accessed':0}};A['bootstrapping-log']={'log-entry':[]}
	if _B in A and A[_B].startswith(_F):A[_B]=sha256_crypt.using(rounds=1000).hash(A[_B][3:])
async def _handle_device_act_code_changed(watched_node_path,jsob,jsob_data_path,nvh):
	A=jsob;assert type(A)==dict
	if jsob_data_path==_C:assert _D in A;B=A[_D]
	else:assert _E in A;B=A[_E]
	if _B in B and B[_B].startswith(_F):B[_B]=sha256_crypt.using(rounds=1000).hash(B[_B][3:])
async def _handle_device_subtree_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_G)
async def _handle_device_somehow_changed(watched_node_path,jsob,jsob_data_path,nvh):raise NotImplementedError(_G)
async def _handle_device_deleted(data_path,nvh):0
def _check_expirations(nvh):0