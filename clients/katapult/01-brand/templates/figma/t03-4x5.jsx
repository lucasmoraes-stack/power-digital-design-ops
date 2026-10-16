const imgHandIphone = "assets/e4b114d2-ba8f-4263-ba39-0a1ee0e821ae.png";
const imgVector12 = "assets/fab5c307-033f-4c2b-8c74-b4303c95a756.svg";
const imgLayer1 = "assets/6831caed-dd75-47d4-85b4-38bb0d85a3d5.svg";

export default function Template03SplitPhoneHand4X5() {
  return (
    <div className="relative size-full" data-node-id="547:1382" data-name="template-03-split-phone-hand-4x5">
      <div className="-translate-y-1/2 absolute bg-[#ed5370] h-[1350px] left-0 top-1/2 w-[490px]" data-node-id="547:1383" data-name="photo-right" />
      <div className="absolute h-[1350px] right-0 top-0 w-[590px]" data-node-id="547:1384">
        <div className="-translate-y-1/2 absolute bg-[#131540] h-[1350px] left-0 top-1/2 w-[590px]" data-node-id="547:1385" data-name="photo-right" />
        <div className="absolute h-[1262.636px] left-[-110px] mix-blend-soft-light top-[284px] w-[2429.41px]" data-node-id="547:1386">
          <div className="absolute inset-[-9.64%_-1.42%_-9.64%_0]">
            <img alt="" className="block max-w-none size-full" src={imgVector12} />
          </div>
        </div>
        <div className="absolute content-stretch flex flex-col h-[1042px] items-center justify-between left-[25px] top-[94px] w-[530px]" data-node-id="547:1387">
          <div className="content-stretch flex flex-col gap-[48px] items-center relative shrink-0 w-[530px]" data-node-id="547:1388" data-name="copy">
            <div className="h-[35px] relative shrink-0 w-[157.198px]" data-node-id="547:1389" data-name="Layer_1">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgLayer1} />
            </div>
            <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Bold'] font-bold leading-[0] not-italic relative shrink-0 text-[82.324px] text-center text-white tracking-[-3.293px] w-[530px]" data-node-id="547:1395">
              <p className="leading-none mb-0">Open the app</p>
              <p className="leading-none mb-0">Find it fast</p>
              <p className="leading-none">Make it yours.</p>
            </div>
            <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] not-italic relative shrink-0 text-[40px] text-[rgba(255,255,255,0.85)] text-center w-[419.254px]" data-node-id="547:1396">
              Browse, apply, and start shopping right from your phone.
            </p>
            <div className="bg-[#ed5370] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1397" data-name="Button">
              <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1397;2485:67">
                Leap Forward
              </p>
            </div>
          </div>
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[#d8d8d8] text-[15px] text-center w-[304.104px]" data-node-id="547:1398">
            Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
          </p>
        </div>
      </div>
      <div className="absolute h-[1258.2px] left-[-165.6px] top-[133.2px] w-[762.3px]" data-node-id="547:1399" data-name="hand-iphone">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <img alt="" className="absolute h-[133.91%] left-0 max-w-none top-[-33.91%] w-[147.38%]" src={imgHandIphone} />
        </div>
      </div>
    </div>
  );
}